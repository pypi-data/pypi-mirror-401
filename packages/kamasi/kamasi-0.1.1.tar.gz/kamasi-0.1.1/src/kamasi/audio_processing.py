"""Audio processing module for Kamasi.

Handles audio manipulation and vocal separation using Demucs.
"""

from pathlib import Path
from typing import Optional
import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import AudioFile, save_audio
from loguru import logger


def separate_vocals(input_path: Path, audio_config: dict) -> Path:
    """Separate vocals from an audio file using Demucs.

    Args:
        input_path: Path to the input audio file
        audio_config: Configuration dictionary containing:
            - model: Demucs model name (e.g., 'htdemucs')
            - device: 'cuda' or 'cpu'
            - separate_vocals: boolean flag

    Returns:
        Path to the separated vocals audio file

    Raises:
        FileNotFoundError: If input file doesn't exist
        RuntimeError: If separation fails
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input audio file not found: {input_path}")

    try:
        # Extract config parameters
        model_name = audio_config.get("model", "htdemucs")
        device = audio_config.get("device", "cpu")

        # Validate device
        if device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA not available, falling back to CPU")
            device = "cpu"

        logger.info(f"Loading Demucs model: {model_name}")

        # Load the pretrained model
        model = get_model(name=model_name)
        model.to(device)
        model.eval()

        logger.info(f"Processing audio file: {input_path.name}")

        # Load audio
        wav = AudioFile(str(input_path)).read(
            streams=0, samplerate=model.samplerate, channels=model.audio_channels
        )

        # Convert to tensor and add batch dimension
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()
        wav = torch.tensor(wav, device=device).unsqueeze(0)

        # Apply model
        with torch.no_grad():
            sources = apply_model(model, wav, device=device)

        # Extract vocals (index depends on model, but typically vocals are at index 3 for htdemucs)
        # Demucs models output: drums, bass, other, vocals
        sources = sources.squeeze(0)
        vocals = sources[3]  # vocals stem

        TMP_DIR = Path("/tmp/kamasi/")

        # Prepare output directory and filename
        output_dir = TMP_DIR / "separated" / input_path.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        vocals_path = TMP_DIR / "vocals.wav"

        # Save vocals
        vocals = vocals.cpu()
        vocals = vocals * ref.std() + ref.mean()

        save_audio(vocals, str(vocals_path), samplerate=model.samplerate)

        logger.success(f"Vocals saved to: {vocals_path}")

        return vocals_path

    except Exception as e:
        error_msg = f"Failed to separate vocals: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e


def get_audio_duration(audio_path: Path) -> Optional[float]:
    """Get the duration of an audio file in seconds.

    Args:
        audio_path: Path to the audio file

    Returns:
        Duration in seconds, or None if unable to determine
    """
    try:
        import torchaudio

        info = torchaudio.info(str(audio_path))
        duration = info.num_frames / info.sample_rate
        return duration
    except Exception as e:
        logger.warning(f"Could not determine audio duration: {e}")
        return None

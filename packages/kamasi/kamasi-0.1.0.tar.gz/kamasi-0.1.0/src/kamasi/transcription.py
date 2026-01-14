"""Transcription module for Kamasi.

Handles speech-to-text conversion using faster-whisper.
"""

from pathlib import Path
from typing import Union
from faster_whisper import WhisperModel
from loguru import logger


def transcribe_audio(audio_path: Union[str, Path], transcription_config: dict) -> str:
    """Transcribe audio to text using faster-whisper.

    Args:
        audio_path: Path to the audio file to transcribe
        transcription_config: Configuration dictionary containing:
            - model_size: Whisper model size (tiny, base, small, medium, large-v3)
            - language: Language code (e.g., 'fr', 'en') or None for auto-detection
            - compute_type: Compute precision ('float16' for GPU, 'int8' for CPU)

    Returns:
        Transcribed text as a single string

    Raises:
        FileNotFoundError: If audio file doesn't exist
        RuntimeError: If transcription fails
    """
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        # Extract config parameters
        model_size = transcription_config.get("model_size", "medium")
        language = transcription_config.get("language")
        compute_type = transcription_config.get("compute_type", "float16")

        # Debug: Show available models
        available_models = [
            "tiny",
            "tiny.en",
            "base",
            "base.en",
            "small",
            "small.en",
            "medium",
            "medium.en",
            "large-v1",
            "large-v2",
            "large-v3",
            "large-v3-turbo",
        ]
        logger.debug(f"Available Whisper models: {', '.join(available_models)}")

        # Smart device selection: use CPU for int8, auto for float16
        device = "cpu" if compute_type == "int8" else "auto"
        logger.info(
            f"Loading Whisper model: {model_size} (compute_type={compute_type}, device={device})"
        )

        # Initialize the Whisper model
        model = WhisperModel(model_size, device=device, compute_type=compute_type)

        logger.info(f"Transcribing audio: {audio_path.name}")

        # Perform transcription
        segments, info = model.transcribe(
            str(audio_path),
            language=language,
            beam_size=5,
            vad_filter=True,  # Use Voice Activity Detection to filter out silence
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        # Log detected language if auto-detected
        if language is None:
            logger.info(
                f"Detected language: {info.language} (probability: {info.language_probability:.2f})"
            )

        # Collect all text segments
        transcribed_text = []
        segment_count = 0

        for segment in segments:
            transcribed_text.append(segment.text.strip())
            segment_count += 1

            # Log progress every 10 segments
            if segment_count % 10 == 0:
                logger.debug(f"Processed {segment_count} segments...")

        # Join all segments into a single text
        full_text = " ".join(transcribed_text)

        logger.success(
            f"Transcription complete: {len(full_text)} characters, {segment_count} segments"
        )

        return full_text

    except Exception as e:
        error_msg = f"Failed to transcribe audio: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e


def transcribe_with_timestamps(
    audio_path: Union[str, Path], transcription_config: dict
) -> list[dict]:
    """Transcribe audio with word-level timestamps.

    Args:
        audio_path: Path to the audio file to transcribe
        transcription_config: Configuration dictionary (same as transcribe_audio)

    Returns:
        List of dictionaries containing:
            - text: Transcribed segment text
            - start: Start timestamp in seconds
            - end: End timestamp in seconds

    Raises:
        FileNotFoundError: If audio file doesn't exist
        RuntimeError: If transcription fails
    """
    audio_path = Path(audio_path)

    logger.debug(f"Current directory: {Path.cwd()}")

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        model_size = transcription_config.get("model_size", "medium")
        language = transcription_config.get("language")
        compute_type = transcription_config.get("compute_type", "float16")

        # Debug: Show available models
        available_models = [
            "tiny",
            "tiny.en",
            "base",
            "base.en",
            "small",
            "small.en",
            "medium",
            "medium.en",
            "large-v1",
            "large-v2",
            "large-v3",
            "large-v3-turbo",
        ]
        logger.debug(f"Available Whisper models: {', '.join(available_models)}")

        # Smart device selection: use CPU for int8, auto for float16
        device = "cpu" if compute_type == "int8" else "auto"
        logger.info(
            f"Loading Whisper model for timestamped transcription: {model_size} (compute_type={compute_type}, device={device})"
        )

        model = WhisperModel(model_size, device=device, compute_type=compute_type)

        logger.info(f"Transcribing audio with timestamps: {audio_path.name}")

        segments, info = model.transcribe(
            str(audio_path),
            language=language,
            beam_size=5,
            vad_filter=True,
            word_timestamps=True,  # Enable word-level timestamps
        )

        timestamped_segments = []
        for segment in segments:
            timestamped_segments.append(
                {
                    "text": segment.text.strip(),
                    "start": segment.start,
                    "end": segment.end,
                }
            )

        logger.success(
            f"Timestamped transcription complete: {len(timestamped_segments)} segments"
        )

        return timestamped_segments

    except Exception as e:
        error_msg = f"Failed to transcribe with timestamps: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

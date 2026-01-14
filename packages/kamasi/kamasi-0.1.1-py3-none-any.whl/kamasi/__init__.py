"""Kamasi - Music lyrics transcription tool.

A functional Python tool for extracting and refining lyrics from audio files
using vocal separation, speech-to-text, and LLM post-processing.
"""

__version__ = "0.1.0"

# Export main functions for cleaner imports
from kamasi.audio_processing import separate_vocals, get_audio_duration
from kamasi.transcription import transcribe_audio, transcribe_with_timestamps
from kamasi.llm_refinement import (
    refine_lyrics,
    refine_lyrics_streaming,
    check_ollama_connection,
    list_available_models,
)

__all__ = [
    "separate_vocals",
    "get_audio_duration",
    "transcribe_audio",
    "transcribe_with_timestamps",
    "refine_lyrics",
    "refine_lyrics_streaming",
    "check_ollama_connection",
    "list_available_models",
]

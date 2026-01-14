# CLAUDE.md - Project Guidelines for Kamasi

This document defines the technical standards, architectural decisions, and conventions for the development of **Kamasi**, a music lyrics transcription tool.

## 🛠 Technical Stack

* **Dependency Manager:** `uv` (mandatory, use `pyproject.toml`).
* **Language:** Python 3.10+
* **Audio Separation:** `demucs` (Meta) for vocal isolation.
* **Transcription:** `faster-whisper` (local models).
* **Post-processing:** `ollama` (via local API for LLM refinement).
* **Interface:** `loguru` for logging.

## 🏗 Architecture & Principles

* **Zero Classes:** The project must follow a **functional programming** paradigm. Use pure functions, dictionaries, and primitive types. Do not use classes like `MusicProcessor` or `TranscriptionEngine`.
* **Modularity:** Strictly separate responsibilities into distinct files:
* `src/kamasi/audio_processing.py`: Audio manipulation and Demucs separation.
* `src/kamasi/transcription.py`: Faster-Whisper logic (STT).
* `src/kamasi/llm_refinement.py`: API calls to Ollama.
* `main.py`: YAML parsing, orchestration and workflow management.


* **Configuration-Driven:** Everything must be controlled by a `config.yaml` file. No hardcoded values (models, paths, URLs) inside the processing functions.

## 📝 Python Best Practices

* **Type Hinting:** All function signatures must be typed (e.g., `def process(path: Path) -> dict:`).
* **Error Handling:** Use explicit `try/except` blocks around heavy tasks (AI/GPU/Filesystem) with clear error messages using `rich.console`.
* **Docstrings:** Provide a concise docstring for every function explaining its role and return value.
* **File Management:** Use `pathlib` for all path manipulations. Ensure GPU resources are handled or logged correctly.

## 🚀 Development Workflow

1. To add a dependency: `uv add <package>`
2. To run the script: `uv run kamasi` (configured via `project.scripts` in `pyproject.toml`)
3. To sync environment: `uv sync`

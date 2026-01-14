# 🎵 Kamasi

**Kamasi** is a local automated music lyric transcription tool. It leverages state-of-the-art AI models to isolate vocals, transcribe them with high precision, and refine the final text using local LLMs.

---

## 🚀 Features

* **Vocal Separation:** Isolate vocals from background music using **Demucs** to ensure the highest transcription accuracy.
* **High-Speed Transcription:** Powered by **Faster-Whisper** for efficient and precise speech-to-text conversion.
* **LLM Refinement:** Automatically fix punctuation, formatting, and transcription hallucinations using **Ollama**.
* **Privacy-First (100% Local):** All processing happens on your machine. No data or audio files are ever uploaded to the cloud.
* **YAML Driven:** Fully customizable workflow via a simple `config.yaml` file.

---

## 🛠 Installation

This project uses [uv](https://github.com/astral-sh/uv) for lightning-fast Python dependency management.

1. **Clone the repository:**
```bash
git clone https://codeberg.org/ley0x/kamasi.git
cd kamasi
```


2. **Install dependencies:**
```bash
uv sync
```


3. **External Requirements:**
* **FFmpeg**: Required for audio processing and conversion.
* **Ollama**: Required if you enable the LLM refinement stage.

---

## ⚙️ Configuration

Create or edit the `config.yaml` file in the root directory to set your preferences:

```yaml
# Note: The input file is now specified as a command-line argument
# Usage: uv run kamasi <audio_file.mp3>

audio:
  separate_vocals: true  # Activer/Désactiver Demucs
  device: "cuda"         # "cuda" pour GPU NVIDIA ou "cpu"
  model: "htdemucs"      # htdemucs, htdemucs_ft, mdx_extra

transcription:
  model_size: "tiny"     # tiny, base, small, medium, large-v3
  language: "fr"         # Code langue (fr, en, etc.) ou null pour auto-detect
  compute_type: "int8"   # float16 pour GPU, int8 pour CPU

refinement:
  enabled: true
  ollama_url: "http://localhost:11434"
  model_name: "mistral-nemo:12b"
  prompt: |
    Write here your instruction for the LLM to follow.
```

---

## 📖 Usage

### Basic Usage

Transcribe an audio file using the default config:

```bash
uv run kamasi audio.mp3
uv run kamasi "path/to/song.mp3"
```

### CLI Options

Specify a custom configuration file:
```bash
uv run kamasi --config custom.yaml audio.mp3
uv run kamasi -c custom.yaml audio.mp3
```

Enable verbose logging (show detailed progress):
```bash
uv run kamasi --verbose audio.mp3
uv run kamasi -v audio.mp3
```

Show version information:
```bash
uv run kamasi --version
```

List available Ollama models:
```bash
uv run kamasi --list-models
uv run kamasi --list-models -c custom.yaml
```

Combine options:
```bash
uv run kamasi -v -c my-config.yaml audio.mp3
```

View help:
```bash
uv run kamasi --help
```

### Batch Processing

Process multiple files:
```bash
for file in input/*.mp3; do
  uv run kamasi "$file"
done
```

The final lyrics will be saved as a `.txt` file in the current directory.

**Note:** By default, only errors are shown. Use `--verbose` / `-v` to see detailed progress including INFO and DEBUG messages.


---

## 📝 Recommendations

Some audio separation models recommandations:
1. htdemucs (current choice) ✅ - Best overall choice
    - Fast processing
    - Excellent vocal separation quality
    - Well-balanced
2. htdemucs_ft - If you want maximum quality and don't mind 4x slower processing
3. mdx_extra - Alternative if htdemucs doesn't work well for your music style


Some ollama models recommandations:
- Llama 3.1 (8B): All types of standard corrections.
- Mistral-Nemo (12B): French language, French songs, rap (slang).
- Qwen 2.5 (14B): Long texts, strict formatting required.
- Gemma 2 (9B): Creativity, poetic or abstract texts.

Some prompt examples:
- French songs:
```
**Rôle** : Tu es un expert en édition musicale et correction de paroles. Voici un texte brut issu d'une transcription automatique. Il contient des erreurs phonétiques (homophones) et de ponctuation.
Tes instructions :
    - Corrige l'orthographe et la grammaire.
    - Déduis les mots mal transcrits en te basant sur le contexte de la phrase et les rimes probables.
    - Ajoute la ponctuation et respecte les sauts de ligne (format paroles de chanson).
    - **IMPORTANT** : Ne réécris pas le style et n'invente pas de nouvelles phrases. Reste fidèle à l'audio original supposé.

Ne donne aucune explication, sors uniquement le texte corrigé.
Texte à corriger :
```

- French songs (rap / urban):
```
**Rôle** :Tu es un expert de la culture Hip-hop, de l'argot urbain (français/anglais) et un éditeur de paroles professionnel.
**Contexte** : Voici une transcription brute d'un morceau de rap générée par une IA. Elle contient des erreurs phonétiques, rate souvent les mots d'argot ou les noms propres, et la mise en page est inexistante.

Tes instructions :
    - **Correction Phonétique Intelligente** : Corrige les mots mal entendus en te basant sur le contexte "Street" et la rime. (Exemple : Si l'audio transcrit "le ter-ter", ne corrige pas en "la terre", garde "le ter-ter").
    - **Respect de la Langue** : NE CORRIGE PAS la grammaire si c'est une faute volontaire de style (ex: "J'ai pas" au lieu de "Je n'ai pas", "C'est nous les meilleurs" au lieu de "Ce sont nous..."). Laisse le verlan et l'argot tels quels.
    - **Structure et Flow** : Formate le texte pour refléter le rythme. Fais des sauts de ligne courts. Essaie d'identifier et de marquer les sections : [Couplet], [Refrain], [Pont], [Outro].
    - **Ad-libs** : Si tu repères des interjections d'ambiance (Yeah, Han, Skrt), mets-les entre parenthèses ou en fin de ligne, ou supprime-les si elles nuisent à la lecture.
    - **Noms Propres** : Sois vigilant sur les noms de rappeurs, de marques, de villes ou de quartiers souvent cités dans le rap.

Contraintes :
    - Ne donne aucune explication avant ou après le texte.
    - Ne censure pas les vulgarités.
    - Affiche uniquement les paroles finales formatées.

Texte brut à traiter :
```

- English songs:
```
Role: You are an expert music editor and lyrics corrector.

Context: Below is raw text generated by an automatic audio transcription tool. It contains phonetic errors (homophones), missing punctuation, and lacks formatting.

Your Instructions:

    Correction: Fix spelling and grammar errors caused by the transcription software.

    Contextual Deduction: Correct mistranscribed words based on the context of the sentence and probable rhymes.

    Formatting: Add proper punctuation and capitalization. Structure the text as song lyrics (short lines, stanzas, spacing between verses).

    Fidelity: IMPORTANT: Do not rewrite the style or change the meaning. Do not invent new lines. Stick as close to the phonetic audio as possible while making it readable.

    Output: Provide only the corrected lyrics. Do not add any conversational text or explanations.

Raw Text to Process:
```

- English songs (rap / urban):
```
**Role**: You are an expert in Hip-Hop culture, AAVE (African American Vernacular English), urban slang, and a professional lyrics editor.
**Context**: Below is a raw transcription of a Rap song. The audio tool struggled with the speed, slang, and flow.

Your Instructions:
    - **Smart Phonetic Correction**: Fix words that were misheard based on "Street" context and rhyme schemes. (e.g., if the text says "trap house," do not change it to "trap mouse").
    - **Respect the Dialect**: DO NOT "fix" the grammar if it is intentional slang or AAVE (e.g., keep "I ain't got no" instead of changing it to "I do not have any"). Preserve contractions and street vernacular.
    - **Structure & Flow**: Format the text to reflect the rhythm (bars). Use short line breaks. Try to identify and label sections if clear: [Verse], [Chorus], [Bridge], [Outro].
    **Ad-libs**: If you detect background ad-libs (Yeah, Uh, Skrt), place them in parentheses (Yeah) or at the end of lines.
    - **Cultural Accuracy**: Be vigilant with proper nouns—names of rappers, luxury brands, cities, or specific neighborhoods often mentioned in Rap.

Constraints:
    - Do not provide any introductory text or summary.
    - Do not censor explicit language or profanity.
    - Output only the final formatted lyrics.

Raw Text to Process:
```

Recommanded AI temperatures: between `0.2` and `0.3`.

---

## 🛠 Project Structure

The project follows a functional programming approach for clarity and modularity:

* `audio_processing.py`: Vocal separation and audio cleaning.
* `transcription.py`: Whisper engine logic.
* `llm_refinement.py`: Ollama API integration.
* `config_loader.py`: YAML settings management.

---

## 🧑‍💻 Development

### Code Quality Tools

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting to maintain consistent code quality.

**Install pre-commit hooks:**
```bash
uvx pre-commit install
```

**Run linting with auto-fix:**
```bash
uv run ruff check --fix .
```

**Format code:**
```bash
uv run ruff format .
```

The pre-commit hook will automatically run ruff checks before each commit. If you need to bypass the hook temporarily, use `git commit --no-verify` (not recommended).

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

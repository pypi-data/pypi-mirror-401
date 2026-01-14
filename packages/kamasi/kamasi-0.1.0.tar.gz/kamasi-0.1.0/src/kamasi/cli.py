import yaml
import sys
from pathlib import Path
from loguru import logger
import typer
import importlib.metadata

# Import your functional modules
from kamasi.audio_processing import separate_vocals
from kamasi.transcription import transcribe_audio
from kamasi.llm_refinement import refine_lyrics

# Create the Typer app instance
app = typer.Typer(
    name="kamasi", help="Music lyrics transcription tool using AI", add_completion=False
)


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""

    logger.remove()
    level = "DEBUG" if verbose else "ERROR"

    logger.add(sys.stderr, level=level)

    logger.debug("Only seen if verbose is True")
    logger.warning("Always seen")


def load_config(path: str = "config.yaml") -> dict:
    """Load and return the YAML configuration."""
    config_path = Path(path)

    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise


def run_transcription_pipeline(config: dict) -> None:
    """Orchestrates the transcription steps."""
    input_path = Path(config["input_file"])

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return
    TMP_DIR = Path("/tmp/kamasi/")
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Audio Separation
    vocals_path: Path
    if config["audio"].get("separate_vocals"):
        logger.info(f"Starting vocal separation for {input_path.name}...")
        vocals_path = separate_vocals(input_path, config["audio"])
        logger.success("Vocals isolated successfully.")
    else:
        vocals_path = input_path

    # 2. Transcription
    logger.info("Starting transcription with Faster-Whisper...")
    raw_text = transcribe_audio(vocals_path, config["transcription"])
    logger.success(f"Transcription complete ({len(raw_text)} characters).")

    # 3. Save raw output
    raw_output_file = TMP_DIR / f"{input_path.stem}.raw.txt"

    raw_output_file.write_text(raw_text, encoding="utf-8")
    logger.info(f"✨ Raw result saved to: {raw_output_file}")

    # 4. LLM Refinement
    final_text = raw_text
    if config["refinement"].get("enabled"):
        logger.info(
            f"Refining lyrics with Ollama ({config['refinement']['model_name']})..."
        )
        final_text = refine_lyrics(raw_text, config["refinement"])
        logger.success("Lyrics refined by AI.")

    # 5. Save Output
    output_file = Path(f"{input_path.stem}.txt")

    output_file.write_text(final_text, encoding="utf-8")
    logger.info(f"✨ Process finished! Result saved to: {output_file}")


def version_callback(value: bool) -> None:
    """Display version information."""
    if value:
        try:
            version = importlib.metadata.version("kamasi")
            typer.echo(f"Kamasi version {version}")
        except importlib.metadata.PackageNotFoundError:
            typer.echo("Kamasi version unknown (development)")
        raise typer.Exit()


def list_models_callback(ctx: typer.Context, value: bool) -> None:
    """List available Ollama models and exit."""
    if not value:
        return

    from kamasi.llm_refinement import list_available_models, check_ollama_connection

    # Configure minimal logging for this operation
    configure_logging(verbose=False)

    try:
        # Get config path from context params if provided, otherwise use default
        config_path = ctx.params.get("config", "config.yaml")
        config_dict = load_config(config_path)
        ollama_url = config_dict.get("refinement", {}).get(
            "ollama_url", "http://localhost:11434"
        )

        if not check_ollama_connection(ollama_url):
            typer.echo(f"Error: Cannot connect to Ollama at {ollama_url}", err=True)
            typer.echo("Make sure Ollama is running: ollama serve", err=True)
            raise typer.Exit(code=1)

        models = list_available_models(ollama_url)

        typer.echo(f"\nAvailable Ollama models at {ollama_url}:")
        for model in models:
            typer.echo(f"  - {model}")

    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        typer.echo(f"Error: Failed to list models: {e}", err=True)
        raise typer.Exit(code=1) from None

    raise typer.Exit()


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    input_file: str = typer.Argument(..., help="Path to the audio file to transcribe"),
    config: str = typer.Option(
        "config.yaml", "--config", "-c", help="Path to the YAML configuration file"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging output"
    ),
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    list_models: bool = typer.Option(
        False,
        "--list-models",
        callback=list_models_callback,
        is_eager=True,
        help="List available Ollama models and exit",
    ),
) -> None:
    """
    Kamasi - Music lyrics transcription tool.

    Transcribe music lyrics from an audio file.

    Orchestrates the full pipeline:
    1. Separate vocals (optional, via Demucs)
    2. Transcribe audio (via Faster-Whisper)
    3. Refine lyrics (optional, via Ollama)
    """
    # Configure logging
    configure_logging(verbose)

    # If a subcommand is invoked, don't run the default transcribe action
    if ctx.invoked_subcommand is not None:
        return

    # Default action: transcribe
    logger.info("Initializing Kamasi...")

    try:
        config_dict = load_config(config)
        config_dict["input_file"] = input_file  # Inject CLI argument
        run_transcription_pipeline(config_dict)

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")
        raise typer.Abort() from None
    except FileNotFoundError as e:
        logger.error(str(e))
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1) from None


def main() -> None:
    """Main entry point for the Kamasi CLI."""
    app()


if __name__ == "__main__":
    main()

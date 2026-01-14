"""LLM refinement module for Kamasi.

Handles post-processing of transcribed lyrics using Ollama for text refinement.
"""

import ollama
from loguru import logger


def check_ollama_connection(ollama_url: str = "http://localhost:11434") -> bool:
    """Check if Ollama server is reachable.

    Args:
        ollama_url: URL of the Ollama API server

    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = ollama.Client(host=ollama_url)
        # Try to list available models as a connection test
        client.list()
        logger.info(f"Successfully connected to Ollama at {ollama_url}")
        return True
    except Exception as e:
        logger.warning(f"Cannot connect to Ollama at {ollama_url}: {str(e)}")
        return False


def list_available_models(ollama_url: str = "http://localhost:11434") -> list[str]:
    """List available models in the Ollama server.

    Args:
        ollama_url: URL of the Ollama API server

    Returns:
        List of model names available on the server

    Raises:
        RuntimeError: If unable to list models
    """
    try:
        client = ollama.Client(host=ollama_url)
        models_response = client.list()

        model_names = [model["model"] for model in models_response.get("models", [])]

        logger.info(f"Available Ollama models: {', '.join(model_names)}")
        return model_names

    except Exception as e:
        error_msg = f"Failed to list Ollama models: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e


def refine_lyrics(raw_text: str, refinement_config: dict) -> str:
    """Refine raw transcribed lyrics using a local LLM via Ollama.

    Args:
        raw_text: Raw transcribed text from Whisper
        refinement_config: Configuration dictionary containing:
            - ollama_url: URL of the Ollama API server
            - model_name: Name of the Ollama model to use
            - prompt: System prompt for the LLM
            - enabled: Whether refinement is enabled

    Returns:
        Refined and structured lyrics

    Raises:
        RuntimeError: If refinement fails or Ollama is unreachable
    """
    if not raw_text or not raw_text.strip():
        logger.warning("Empty text provided for refinement, returning as-is")
        return raw_text

    try:
        # Extract config parameters
        model_name = refinement_config.get("model_name", "llama3")
        system_prompt = refinement_config.get("prompt", "")
        ollama_url = refinement_config.get("ollama_url", "http://localhost:11434")

        # check if ollama is reachable
        if not check_ollama_connection(ollama_url):
            logger.warning("Ollama server not reachable, returning raw text")
            return raw_text

        # log available models
        available_models = list_available_models(ollama_url)

        # check if model is available
        if model_name not in available_models:
            logger.warning(f"Model {model_name} not available, returning raw text")
            return raw_text

        logger.info(f"Refining lyrics with Ollama model: {model_name}")
        logger.debug(f"Ollama URL: {ollama_url}")
        logger.debug(f"Raw text length: {len(raw_text)} characters")

        # Create Ollama client
        client = ollama.Client(host=ollama_url)

        # Prepare the full prompt with the raw text
        full_prompt = f"{system_prompt}\n\n{raw_text}"

        # Call the Ollama API
        response = client.generate(
            model=model_name, prompt=full_prompt, options={"temperature": 0.3}
        )

        # Extract the refined text from response
        refined_text = response["response"].strip()

        logger.success(f"Lyrics refined successfully ({len(refined_text)} characters)")

        return refined_text

    except ollama.ResponseError as e:
        error_msg = f"Ollama API error: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

    except ollama.RequestError as e:
        error_msg = f"Failed to connect to Ollama server at {ollama_url}: {str(e)}"
        logger.error(error_msg)
        logger.error("Make sure Ollama is running: ollama serve")
        raise RuntimeError(error_msg) from e

    except Exception as e:
        error_msg = f"Failed to refine lyrics: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e


def refine_lyrics_streaming(raw_text: str, refinement_config: dict) -> str:
    """Refine lyrics with streaming output for real-time feedback.

    Args:
        raw_text: Raw transcribed text from Whisper
        refinement_config: Configuration dictionary (same as refine_lyrics)

    Returns:
        Refined and structured lyrics

    Raises:
        RuntimeError: If refinement fails or Ollama is unreachable
    """
    if not raw_text or not raw_text.strip():
        logger.warning("Empty text provided for refinement, returning as-is")
        return raw_text

    try:
        model_name = refinement_config.get("model_name", "llama3")
        system_prompt = refinement_config.get("prompt", "")
        ollama_url = refinement_config.get("ollama_url", "http://localhost:11434")

        logger.info(f"Refining lyrics with streaming from model: {model_name}")

        client = ollama.Client(host=ollama_url)

        full_prompt = f"{system_prompt}\n\n{raw_text}"

        # Stream the response
        refined_chunks = []
        for chunk in client.generate(model=model_name, prompt=full_prompt, stream=True):
            response_text = chunk["response"]
            refined_chunks.append(response_text)
            # Optionally print chunks in real-time
            # print(response_text, end='', flush=True)

        refined_text = "".join(refined_chunks).strip()

        logger.success(
            f"Lyrics refined with streaming ({len(refined_text)} characters)"
        )

        return refined_text

    except Exception as e:
        error_msg = f"Failed to refine lyrics with streaming: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e

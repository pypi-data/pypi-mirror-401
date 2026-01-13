"""Centralized configuration for tilde.

This module provides unified configuration for LLM and embedding settings
across the entire tilde project. Uses Google Gemini by default for both
LLM calls and embeddings, requiring only GOOGLE_API_KEY.

Configuration is loaded from (in priority order):
1. Environment variables (highest priority)
2. ~/.tilde/config.yaml file
3. Built-in defaults (lowest priority)
"""

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


# Default config file location
CONFIG_FILE_PATH = Path.home() / ".tilde" / "config.yaml"

# Default values
DEFAULTS = {
    "llm_model": "gemini-3-flash-preview",
    "llm_temperature": 0.7,
    "embedding_model": "gemini-embedding-001",
    "embedding_dimensions": 768,
    "storage_backend": "yaml",
}


@dataclass
class TildeConfig:
    """Configuration for tilde LLM and embedding settings.
    
    Uses Google Gemini by default. Set GOOGLE_API_KEY environment variable.
    Falls back to OpenAI if OPENAI_API_KEY is set and Google key is not.
    
    Configuration is loaded from ~/.tilde/config.yaml and can be overridden
    via environment variables.
    """
    
    # LLM settings
    llm_model: str = DEFAULTS["llm_model"]
    llm_temperature: float = DEFAULTS["llm_temperature"]
    
    # Embedding settings (for semantic search/Mem0)
    embedding_model: str = DEFAULTS["embedding_model"]
    embedding_dimensions: int = DEFAULTS["embedding_dimensions"]
    
    # Storage settings
    storage_backend: str = DEFAULTS["storage_backend"]
    
    # API keys (populated from environment, never saved to file)
    google_api_key: str | None = field(default=None, repr=False)
    openai_api_key: str | None = field(default=None, repr=False)
    
    def __post_init__(self) -> None:
        """Load API keys from environment if not provided."""
        if self.google_api_key is None:
            self.google_api_key = (
                os.environ.get("GOOGLE_API_KEY") or 
                os.environ.get("GEMINI_API_KEY")
            )
        if self.openai_api_key is None:
            self.openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    @property
    def provider(self) -> str:
        """Get the active provider based on available API keys."""
        if self.google_api_key:
            return "google"
        if self.openai_api_key:
            return "openai"
        raise RuntimeError(
            "No API key found. Set GOOGLE_API_KEY environment variable. "
            "Alternatively, set OPENAI_API_KEY for OpenAI backend."
        )
    
    @property
    def api_key(self) -> str:
        """Get the API key for the active provider."""
        if self.google_api_key:
            return self.google_api_key
        if self.openai_api_key:
            return self.openai_api_key
        raise RuntimeError("No API key available")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary (excludes API keys for saving)."""
        return {
            "llm_model": self.llm_model,
            "llm_temperature": self.llm_temperature,
            "embedding_model": self.embedding_model,
            "embedding_dimensions": self.embedding_dimensions,
            "storage_backend": self.storage_backend,
        }


def load_config_file(path: Path | None = None) -> dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        path: Path to config file (default: ~/.tilde/config.yaml)
        
    Returns:
        Dictionary of config values, empty dict if file doesn't exist
    """
    path = path or CONFIG_FILE_PATH
    
    if not path.exists():
        return {}
    
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_config(config: TildeConfig, path: Path | None = None) -> Path:
    """Save configuration to YAML file.
    
    Note: API keys are NOT saved to the file for security.
    
    Args:
        config: TildeConfig instance to save
        path: Path to save to (default: ~/.tilde/config.yaml)
        
    Returns:
        Path where config was saved
    """
    path = path or CONFIG_FILE_PATH
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save config (excluding API keys)
    data = config.to_dict()
    
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    return path


@lru_cache(maxsize=1)
def get_config() -> TildeConfig:
    """Get the global tilde configuration (cached).
    
    Configuration loading priority:
    1. Environment variables (highest priority)
    2. ~/.tilde/config.yaml file
    3. Built-in defaults (lowest priority)
    
    Environment variables:
        GOOGLE_API_KEY: Google/Gemini API key
        TILDE_LLM_MODEL: LLM model name
        TILDE_EMBEDDING_MODEL: Embedding model name
        TILDE_STORAGE: Storage backend
    """
    # Load from file first
    file_config = load_config_file()
    
    # Build config with file values as defaults, env vars as overrides
    return TildeConfig(
        llm_model=os.environ.get(
            "TILDE_LLM_MODEL", 
            file_config.get("llm_model", DEFAULTS["llm_model"])
        ),
        llm_temperature=float(
            file_config.get("llm_temperature", DEFAULTS["llm_temperature"])
        ),
        embedding_model=os.environ.get(
            "TILDE_EMBEDDING_MODEL",
            file_config.get("embedding_model", DEFAULTS["embedding_model"])
        ),
        embedding_dimensions=int(
            file_config.get("embedding_dimensions", DEFAULTS["embedding_dimensions"])
        ),
        storage_backend=os.environ.get(
            "TILDE_STORAGE",
            file_config.get("storage_backend", DEFAULTS["storage_backend"])
        ),
    )


def reset_config() -> None:
    """Clear the cached config (useful after saving new config)."""
    get_config.cache_clear()


def call_llm(prompt: str, model: str | None = None) -> str:
    """Call an LLM to process the prompt.
    
    Uses the configured provider (Google Gemini by default).
    
    Args:
        prompt: The prompt to send to the LLM
        model: Optional model override (uses config default if not provided)
        
    Returns:
        The LLM response text
        
    Raises:
        RuntimeError: If no API key is available or SDK is not installed
    """
    config = get_config()
    model = model or config.llm_model
    
    if config.provider == "google":
        try:
            from google import genai
            
            client = genai.Client(api_key=config.google_api_key)
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            return response.text or ""
        except ImportError:
            raise RuntimeError(
                "google-genai is required. Install with: uv add google-genai"
            )
    
    elif config.provider == "openai":
        try:
            from openai import OpenAI
            
            # Map common Gemini model names to OpenAI equivalents
            openai_model = _map_to_openai_model(model)
            
            client = OpenAI(api_key=config.openai_api_key)
            response = client.chat.completions.create(
                model=openai_model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content or ""
        except ImportError:
            raise RuntimeError(
                "openai is required. Install with: uv add openai"
            )
    
    raise RuntimeError(f"Unknown provider: {config.provider}")


def get_embedding(text: str, model: str | None = None) -> list[float]:
    """Get embedding vector for text.
    
    Uses Google gemini-embedding-001 by default (768 dimensions).
    Falls back to OpenAI text-embedding-3-small if using OpenAI provider.
    
    Args:
        text: Text to embed
        model: Optional model override
        
    Returns:
        List of floats representing the embedding vector
    """
    config = get_config()
    model = model or config.embedding_model
    
    if config.provider == "google":
        try:
            from google import genai
            
            client = genai.Client(api_key=config.google_api_key)
            response = client.models.embed_content(
                model=model,
                contents=text,
            )
            return response.embeddings[0].values
        except ImportError:
            raise RuntimeError(
                "google-genai is required. Install with: uv add google-genai"
            )
    
    elif config.provider == "openai":
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=config.openai_api_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
            )
            return response.data[0].embedding
        except ImportError:
            raise RuntimeError(
                "openai is required. Install with: uv add openai"
            )
    
    raise RuntimeError(f"Unknown provider: {config.provider}")


def _map_to_openai_model(model: str) -> str:
    """Map Gemini model names to OpenAI equivalents."""
    mapping = {
        "gemini-3-flash-preview": "gpt-4o-mini",
        "gemini-1.5-pro": "gpt-4o",
        "gemini-1.5-flash": "gpt-4o-mini",
    }
    return mapping.get(model, model)

import dns.resolver
import logging
import yaml
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from fastapi import Request
from typing import Dict, Optional

class TaskStatus(str, Enum):
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"

class FilterType(str, Enum):
    RAW = "raw"
    FIT = "fit"
    BM25 = "bm25"
    LLM = "llm"

def load_config() -> Dict:
    """Load and return application configuration with environment variable overrides."""
    # Select config file based on environment
    env = os.getenv("PYTHON_ENV", "production")
    config_filename = "config.dev.yml" if env == "development" else "config.yml"
    config_path = Path(__file__).parent / config_filename
    
    logging.info(f"Loading configuration from: {config_filename} (PYTHON_ENV={env})")
    
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    
    # Override LLM provider from environment if set
    llm_provider = os.environ.get("LLM_PROVIDER")
    if llm_provider:
        config["llm"]["provider"] = llm_provider
        logging.info(f"LLM provider overridden from environment: {llm_provider}")
    
    # Also support direct API key from environment if the provider-specific key isn't set
    llm_api_key = os.environ.get("LLM_API_KEY")
    if llm_api_key and "api_key" not in config["llm"]:
        config["llm"]["api_key"] = llm_api_key
        logging.info("LLM API key loaded from LLM_API_KEY environment variable")
    
    return config

def setup_logging(config: Dict) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=config["logging"]["level"],
        format=config["logging"]["format"]
    )

def get_base_url(request: Request) -> str:
    """Get base URL including scheme and host."""
    return f"{request.url.scheme}://{request.url.netloc}"

def is_task_id(value: str) -> bool:
    """Check if the value matches task ID pattern."""
    return value.startswith("llm_") and "_" in value

def datetime_handler(obj: any) -> Optional[str]:
    """Handle datetime serialization for JSON."""
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def should_cleanup_task(created_at: str, ttl_seconds: int = 3600) -> bool:
    """Check if task should be cleaned up based on creation time."""
    created = datetime.fromisoformat(created_at)
    return (datetime.now() - created).total_seconds() > ttl_seconds

def decode_redis_hash(hash_data: Dict[bytes, bytes]) -> Dict[str, str]:
    """Decode Redis hash data from bytes to strings."""
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in hash_data.items()}



def get_llm_api_key(config: Dict, provider: Optional[str] = None) -> str:
    """Get the appropriate API key based on the LLM provider.
    
    Args:
        config: The application configuration dictionary
        provider: Optional provider override (e.g., "openai/gpt-4")
    
    Returns:
        The API key for the provider, or empty string if not found
    """
        
    # Use provided provider or fall back to config
    if not provider:
        provider = config["llm"]["provider"]
    
    # Check if direct API key is configured
    if "api_key" in config["llm"]:
        return config["llm"]["api_key"]
    
    # Extract provider name from the provider string (e.g., "deepseek" from "deepseek/deepseek-chat")
    provider_name = provider.split("/")[0].upper() if "/" in provider else provider.upper()
    
    # Mapping of provider names to their environment variable names
    provider_env_map = {
        "OPENAI": "OPENAI_API_KEY",
        "DEEPSEEK": "DEEPSEEK_API_KEY",
        "ANTHROPIC": "ANTHROPIC_API_KEY",
        "GROQ": "GROQ_API_KEY",
        "TOGETHER": "TOGETHER_API_KEY",
        "MISTRAL": "MISTRAL_API_KEY",
        "GEMINI": "GEMINI_API_TOKEN",
    }
    
    # Try to get the environment variable for this specific provider
    env_var_name = provider_env_map.get(provider_name)
    if env_var_name:
        api_key = os.environ.get(env_var_name, "")
        if api_key:
            return api_key
    
    # Fall back to the configured api_key_env if no match
    return os.environ.get(config["llm"].get("api_key_env", ""), "")


def validate_llm_provider(config: Dict, provider: Optional[str] = None) -> tuple[bool, str]:
    """Validate that the LLM provider has an associated API key.
    
    Args:
        config: The application configuration dictionary
        provider: Optional provider override (e.g., "openai/gpt-4")
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Use provided provider or fall back to config
    if not provider:
        provider = config["llm"]["provider"]
    
    # Get the API key for this provider
    api_key = get_llm_api_key(config, provider)
    
    if not api_key:
        return False, f"No API key found for provider '{provider}'. Please set the appropriate environment variable."
    
    return True, ""


def verify_email_domain(email: str) -> bool:
    try:
        domain = email.split('@')[1]
        # Try to resolve MX records for the domain.
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except Exception as e:
        return False
"""Factory for creating LLM providers."""

import os
from typing import Union

from .base import LLMProvider
from .models import ChatModel
from .openai_provider import OpenAIProvider
from .transformers_provider import TransformersProvider


# ═══════════════════════════════════════════════════════════════════════════════
# Configuration - Single source of truth
# ═══════════════════════════════════════════════════════════════════════════════

# Default model alias
DEFAULT_MODEL = "fireworks:accounts/fireworks/models/minimax-m2p1"

# Default API key environment variable (used by default model)
DEFAULT_API_KEY_ENV = "FIREWORKS_API_KEY"


# ═══════════════════════════════════════════════════════════════════════════════
# Factory functions
# ═══════════════════════════════════════════════════════════════════════════════


def get_provider(model: Union[str, ChatModel] = DEFAULT_MODEL) -> LLMProvider:
    """
    Get an LLM provider for the specified model.

    Uses OpenAI SDK with provider-specific base URLs for OpenAI, Anthropic, and Fireworks.
    For local models, uses HuggingFace Transformers.

    Args:
        model: Model specification - ChatModel enum or alias
            Examples:
                - ChatModel.ANTHROPIC_CLAUDE_HAIKU_4
                - "haiku", "sonnet", "opus"
                - "gpt-4o-mini"
                - "minimax"
                - "local:Qwen/Qwen2.5-1.5B-Instruct"
                - "transformers:microsoft/Phi-3-mini-4k-instruct"

    Returns:
        LLMProvider instance

    Raises:
        ValueError: If model string not recognized
    """
    # Handle local/transformers prefix for local models
    if isinstance(model, str) and (model.startswith("local:") or model.startswith("transformers:")):
        return TransformersProvider(model)

    # Handle ChatModel enum directly
    if isinstance(model, ChatModel):
        return OpenAIProvider(model)

    # Try to parse as ChatModel
    parsed = ChatModel.from_string(model)
    if parsed:
        return OpenAIProvider(parsed)

    # Assume it's a raw model string
    return OpenAIProvider(model)


def get_default_model() -> ChatModel:
    """Get the default model."""
    return ChatModel.from_string(DEFAULT_MODEL) or ChatModel.get_default()


def get_default_api_key() -> str | None:
    """Get the default API key from environment."""
    return os.environ.get(DEFAULT_API_KEY_ENV)


def list_available_models() -> list[dict]:
    """List all available models."""
    return ChatModel.list_all()

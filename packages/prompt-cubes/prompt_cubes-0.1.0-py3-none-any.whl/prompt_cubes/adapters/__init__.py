"""
Schema adapters for different LLM providers.

Script: __init__.py
Created: 2026-01-13
Purpose: Adapter exports and registry
Keywords: adapters, schema, llm, providers
Status: active
"""

from typing import Type

from .base import SchemaAdapter
from .gemini import GeminiAdapter
from .openai import OpenAIAdapter
from .anthropic import AnthropicAdapter

__all__ = [
    "SchemaAdapter",
    "GeminiAdapter",
    "OpenAIAdapter",
    "AnthropicAdapter",
    "get_adapter",
    "ADAPTERS",
]

# Adapter registry
ADAPTERS: dict[str, Type[GeminiAdapter] | Type[OpenAIAdapter] | Type[AnthropicAdapter]] = {
    "gemini": GeminiAdapter,
    "openai": OpenAIAdapter,
    "anthropic": AnthropicAdapter,
}


def get_adapter(provider: str) -> SchemaAdapter:
    """Get adapter instance by provider name.

    Args:
        provider: Provider name ('gemini', 'openai', 'anthropic')

    Returns:
        Adapter instance

    Raises:
        ValueError: If provider is not supported
    """
    if provider not in ADAPTERS:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(ADAPTERS.keys())}")
    return ADAPTERS[provider]()

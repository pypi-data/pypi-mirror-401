"""
Base protocol for schema adapters.

Script: base.py
Created: 2026-01-13
Purpose: Protocol definition for LLM provider schema adapters
Keywords: adapters, protocol, schema, llm
Status: active
"""

from typing import Protocol, Dict, Any


class SchemaAdapter(Protocol):
    """Protocol for LLM provider schema adapters.

    Each adapter converts the internal Gemini-compatible schema format
    to the format expected by a specific LLM provider.
    """

    def adapt(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Convert internal schema format to provider-specific format.

        Args:
            schema: Internal schema (Gemini response_schema format)

        Returns:
            Provider-specific schema format
        """
        ...

    @property
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'gemini', 'openai', 'anthropic')."""
        ...

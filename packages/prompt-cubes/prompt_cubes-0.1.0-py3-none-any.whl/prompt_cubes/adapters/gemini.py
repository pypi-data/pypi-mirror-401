"""
Gemini schema adapter - passthrough (internal format matches Gemini).

Script: gemini.py
Created: 2026-01-13
Purpose: Gemini response_schema format adapter
Keywords: adapters, gemini, schema
Status: active
"""

from typing import Dict, Any


class GeminiAdapter:
    """Gemini response_schema format adapter (default/passthrough).

    The internal schema format is Gemini-compatible, so this adapter
    simply passes through the schema unchanged.
    """

    @property
    def provider_name(self) -> str:
        return "gemini"

    def adapt(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Gemini format is our internal format - passthrough.

        Args:
            schema: Internal schema

        Returns:
            Same schema (Gemini-compatible)
        """
        return schema

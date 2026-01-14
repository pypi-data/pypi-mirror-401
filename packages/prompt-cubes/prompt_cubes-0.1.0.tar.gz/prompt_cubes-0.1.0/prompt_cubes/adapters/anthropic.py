"""
Anthropic tool use schema adapter.

Script: anthropic.py
Created: 2026-01-13
Purpose: Convert internal schema to Anthropic tool use format
Keywords: adapters, anthropic, schema, tool-use
Status: active
"""

from typing import Dict, Any


class AnthropicAdapter:
    """Anthropic tool use format adapter.

    Converts internal Gemini-style schema to Anthropic's tool use format.
    """

    def __init__(self, tool_name: str = "response"):
        """Initialize adapter.

        Args:
            tool_name: Name for the tool in Anthropic format
        """
        self.tool_name = tool_name

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def adapt(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to Anthropic tool use format.

        Args:
            schema: Internal schema (Gemini format)

        Returns:
            Anthropic tool use format:
            {
                "name": "response",
                "description": "Structured response",
                "input_schema": { ...schema... }
            }
        """
        return {
            "name": self.tool_name,
            "description": "Structured response from prompt",
            "input_schema": schema
        }

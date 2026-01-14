"""
OpenAI function calling schema adapter.

Script: openai.py
Created: 2026-01-13
Purpose: Convert internal schema to OpenAI function calling format
Keywords: adapters, openai, schema, function-calling
Status: active
"""

from typing import Dict, Any


class OpenAIAdapter:
    """OpenAI function calling format adapter.

    Converts internal Gemini-style schema to OpenAI's function calling format
    with structured outputs (strict mode).
    """

    def __init__(self, function_name: str = "response"):
        """Initialize adapter.

        Args:
            function_name: Name for the function in OpenAI format
        """
        self.function_name = function_name

    @property
    def provider_name(self) -> str:
        return "openai"

    def adapt(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to OpenAI function calling format.

        Args:
            schema: Internal schema (Gemini format)

        Returns:
            OpenAI function calling format:
            {
                "type": "function",
                "function": {
                    "name": "response",
                    "description": "Structured response",
                    "parameters": { ...schema... },
                    "strict": True
                }
            }
        """
        return {
            "type": "function",
            "function": {
                "name": self.function_name,
                "description": "Structured response from prompt",
                "parameters": schema,
                "strict": True  # Enable structured outputs
            }
        }

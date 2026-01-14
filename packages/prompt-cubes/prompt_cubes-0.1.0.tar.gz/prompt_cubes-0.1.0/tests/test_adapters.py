"""Tests for schema adapters."""

import pytest
from prompt_cubes import (
    GeminiAdapter,
    OpenAIAdapter,
    AnthropicAdapter,
    get_adapter,
)


class TestGeminiAdapter:
    """Test GeminiAdapter (passthrough)."""

    def test_provider_name(self):
        """Test provider name."""
        adapter = GeminiAdapter()
        assert adapter.provider_name == "gemini"

    def test_passthrough(self):
        """Test that schema is passed through unchanged."""
        adapter = GeminiAdapter()
        schema = {
            "type": "object",
            "properties": {"response": {"type": "string"}},
            "required": ["response"]
        }

        result = adapter.adapt(schema)
        assert result == schema


class TestOpenAIAdapter:
    """Test OpenAIAdapter."""

    def test_provider_name(self):
        """Test provider name."""
        adapter = OpenAIAdapter()
        assert adapter.provider_name == "openai"

    def test_function_calling_format(self):
        """Test conversion to OpenAI function calling format."""
        adapter = OpenAIAdapter()
        schema = {
            "type": "object",
            "properties": {"response": {"type": "string"}},
            "required": ["response"]
        }

        result = adapter.adapt(schema)

        assert result["type"] == "function"
        assert "function" in result
        assert result["function"]["name"] == "response"
        assert result["function"]["parameters"] == schema
        assert result["function"]["strict"] is True

    def test_custom_function_name(self):
        """Test custom function name."""
        adapter = OpenAIAdapter(function_name="custom_response")
        result = adapter.adapt({"type": "object", "properties": {}})

        assert result["function"]["name"] == "custom_response"


class TestAnthropicAdapter:
    """Test AnthropicAdapter."""

    def test_provider_name(self):
        """Test provider name."""
        adapter = AnthropicAdapter()
        assert adapter.provider_name == "anthropic"

    def test_tool_use_format(self):
        """Test conversion to Anthropic tool use format."""
        adapter = AnthropicAdapter()
        schema = {
            "type": "object",
            "properties": {"response": {"type": "string"}},
            "required": ["response"]
        }

        result = adapter.adapt(schema)

        assert result["name"] == "response"
        assert result["input_schema"] == schema
        assert "description" in result

    def test_custom_tool_name(self):
        """Test custom tool name."""
        adapter = AnthropicAdapter(tool_name="custom_tool")
        result = adapter.adapt({"type": "object", "properties": {}})

        assert result["name"] == "custom_tool"


class TestGetAdapter:
    """Test get_adapter factory function."""

    def test_get_gemini_adapter(self):
        """Test getting Gemini adapter."""
        adapter = get_adapter("gemini")
        assert adapter.provider_name == "gemini"

    def test_get_openai_adapter(self):
        """Test getting OpenAI adapter."""
        adapter = get_adapter("openai")
        assert adapter.provider_name == "openai"

    def test_get_anthropic_adapter(self):
        """Test getting Anthropic adapter."""
        adapter = get_adapter("anthropic")
        assert adapter.provider_name == "anthropic"

    def test_unknown_provider_raises(self):
        """Test that unknown provider raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_adapter("unknown")

        assert "Unknown provider" in str(exc_info.value)
        assert "unknown" in str(exc_info.value)

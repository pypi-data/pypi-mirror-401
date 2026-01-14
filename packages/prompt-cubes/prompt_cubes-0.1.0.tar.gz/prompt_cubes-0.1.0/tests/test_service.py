"""Tests for PromptService."""

import pytest
from prompt_cubes import PromptService, IterationContext


class TestPromptService:
    """Test PromptService functionality."""

    def test_build_basic_prompt(self, service, basic_context):
        """Test building a basic prompt bundle."""
        bundle = service.build(basic_context)

        assert bundle.system_prompt is not None
        assert bundle.user_prompt is not None
        assert len(bundle.system_prompt) > 0
        assert len(bundle.user_prompt) > 0

    def test_build_includes_role_content(self, service, basic_context):
        """Test that built prompt includes role cube content."""
        bundle = service.build(basic_context)

        # Should include ROLE_CHATBOT content
        assert "helpful" in bundle.system_prompt.lower()
        assert "chatbot" in bundle.system_prompt.lower()

    def test_template_substitution(self, service, basic_context):
        """Test that template variables are substituted."""
        basic_context.user_query = "What is Python?"
        bundle = service.build(basic_context)

        # USER_QUERY template should substitute {{user_query}}
        assert "What is Python?" in bundle.user_prompt

    def test_schema_merging(self, service, basic_context):
        """Test that schemas from cubes are merged."""
        bundle = service.build(basic_context)

        assert bundle.response_schema["type"] == "object"
        assert "properties" in bundle.response_schema
        # CONTEXT_SESSION defines 'response' and 'needs_clarification' schema fields
        assert "response" in bundle.response_schema["properties"]
        assert "needs_clarification" in bundle.response_schema["properties"]

    def test_model_config(self, service, basic_context):
        """Test model configuration is set correctly."""
        bundle = service.build(basic_context)

        assert bundle.model_config is not None
        assert bundle.model_config.model_name is not None

    def test_dump_info(self, service, basic_context):
        """Test dump_info contains debugging information."""
        bundle = service.build(basic_context)

        assert "mode" in bundle.dump_info
        assert "agent_type" in bundle.dump_info
        assert "iteration" in bundle.dump_info
        assert "cubes" in bundle.dump_info
        assert bundle.dump_info["mode"] == "chatbot"

    def test_to_llm_config(self, service, basic_context):
        """Test to_llm_config method returns valid config."""
        bundle = service.build(basic_context)
        config = bundle.to_llm_config()

        assert "model" in config
        assert "system_instruction" in config
        assert "temperature" in config
        assert "response_schema" in config

    def test_different_modes(self, examples_path):
        """Test building prompts with different modes."""
        service = PromptService(cubes_path=str(examples_path))

        # Default mode
        context_default = IterationContext(
            mode="chatbot", agent_type="default", iteration=1, max_iterations=3
        )
        bundle_default = service.build(context_default)

        # Concise mode
        context_concise = IterationContext(
            mode="chatbot", agent_type="concise", iteration=1, max_iterations=3
        )
        bundle_concise = service.build(context_concise)

        # Concise mode should include MODE_CONCISE content
        assert "concise" in bundle_concise.system_prompt.lower()

    def test_list_cubes(self, service):
        """Test listing available cubes."""
        cubes = service.list_cubes()

        assert isinstance(cubes, list)
        assert len(cubes) >= 4
        assert "ROLE_CHATBOT" in cubes

    def test_get_cube_content(self, service):
        """Test getting cube content by ID."""
        content = service.get_cube_content("ROLE_CHATBOT")

        assert content is not None
        assert "helpful" in content.lower()

    def test_from_config_factory(self, examples_path):
        """Test from_config factory method."""
        service = PromptService.from_config(str(examples_path))
        cubes = service.list_cubes()

        assert len(cubes) >= 4

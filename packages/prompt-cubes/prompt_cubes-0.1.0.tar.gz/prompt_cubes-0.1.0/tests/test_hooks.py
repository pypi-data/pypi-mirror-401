"""Tests for hooks system."""

import pytest
from prompt_cubes import PromptService, IterationContext, HookRunner, PromptBundle, PromptCube, ModelConfig


class TestHookRunner:
    """Test HookRunner functionality."""

    def test_pre_build_hook_modifies_context(self):
        """Test that pre_build hooks can modify context."""
        def add_template_var(context: IterationContext) -> IterationContext:
            context.template_vars["custom_var"] = "custom_value"
            return context

        runner = HookRunner(hooks={"pre_build": [add_template_var]})

        context = IterationContext(
            mode="test", agent_type="default", iteration=1, max_iterations=3
        )
        modified = runner.run_pre_build(context)

        assert modified.template_vars.get("custom_var") == "custom_value"

    def test_post_cube_load_hook_modifies_content(self):
        """Test that post_cube_load hooks can modify content."""
        def uppercase_content(cube: PromptCube, content: str) -> str:
            return content.upper()

        runner = HookRunner(hooks={"post_cube_load": [uppercase_content]})

        cube = PromptCube(id="TEST", target="system", priority=1, category="test")
        result = runner.run_post_cube_load(cube, "hello world")

        assert result == "HELLO WORLD"

    def test_post_template_hook_modifies_content(self):
        """Test that post_template hooks can modify rendered content."""
        def add_suffix(content: str, target: str) -> str:
            return f"{content}\n<!-- {target} -->"

        runner = HookRunner(hooks={"post_template": [add_suffix]})
        result = runner.run_post_template("Hello", "system")

        assert "<!-- system -->" in result

    def test_post_build_hook_modifies_bundle(self):
        """Test that post_build hooks can modify bundle."""
        def add_metadata(bundle: PromptBundle) -> PromptBundle:
            bundle.dump_info["hook_processed"] = True
            return bundle

        runner = HookRunner(hooks={"post_build": [add_metadata]})

        bundle = PromptBundle(
            system_prompt="sys",
            user_prompt="usr",
            model_config=ModelConfig(),
            response_schema={},
            dump_info={}
        )
        modified = runner.run_post_build(bundle)

        assert modified.dump_info.get("hook_processed") is True

    def test_hook_error_handling_graceful(self):
        """Test that hook errors are handled gracefully by default."""
        def bad_hook(context: IterationContext) -> IterationContext:
            raise ValueError("Hook error!")

        runner = HookRunner(hooks={"pre_build": [bad_hook]}, fail_on_error=False)

        context = IterationContext(
            mode="test", agent_type="default", iteration=1, max_iterations=3
        )
        # Should not raise, should log error
        result = runner.run_pre_build(context)
        assert result is context

    def test_hook_error_handling_strict(self):
        """Test that hook errors are raised when fail_on_error=True."""
        def bad_hook(context: IterationContext) -> IterationContext:
            raise ValueError("Hook error!")

        runner = HookRunner(hooks={"pre_build": [bad_hook]}, fail_on_error=True)

        context = IterationContext(
            mode="test", agent_type="default", iteration=1, max_iterations=3
        )

        with pytest.raises(Exception):  # HookError wraps the original
            runner.run_pre_build(context)

    def test_multiple_hooks_chain(self):
        """Test that multiple hooks are chained correctly."""
        def hook1(context: IterationContext) -> IterationContext:
            context.template_vars["hook1"] = True
            return context

        def hook2(context: IterationContext) -> IterationContext:
            context.template_vars["hook2"] = True
            return context

        runner = HookRunner(hooks={"pre_build": [hook1, hook2]})

        context = IterationContext(
            mode="test", agent_type="default", iteration=1, max_iterations=3
        )
        modified = runner.run_pre_build(context)

        assert modified.template_vars.get("hook1") is True
        assert modified.template_vars.get("hook2") is True


class TestPromptServiceWithHooks:
    """Test PromptService with hooks integration."""

    def test_service_with_hooks(self, examples_path):
        """Test that hooks are called during build."""
        call_log = []

        def log_pre_build(context: IterationContext) -> IterationContext:
            call_log.append("pre_build")
            return context

        def log_post_build(bundle: PromptBundle) -> PromptBundle:
            call_log.append("post_build")
            return bundle

        service = PromptService(
            cubes_path=str(examples_path),
            hooks={
                "pre_build": [log_pre_build],
                "post_build": [log_post_build]
            }
        )

        context = IterationContext(
            mode="chatbot", agent_type="default", iteration=1, max_iterations=3
        )
        service.build(context)

        assert "pre_build" in call_log
        assert "post_build" in call_log

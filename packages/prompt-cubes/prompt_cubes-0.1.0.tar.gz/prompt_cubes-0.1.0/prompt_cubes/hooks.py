"""
Hook protocols and execution for prompt assembly pipeline.

Script: hooks.py
Created: 2026-01-13
Purpose: Middleware/hooks system for prompt assembly
Keywords: hooks, middleware, pipeline, prompts
Status: active
"""

from typing import Protocol, Dict, Any, List, Callable, Optional
import logging

from .models import IterationContext, PromptCube, PromptBundle
from .exceptions import HookError

logger = logging.getLogger(__name__)


# === Hook Protocols ===

class PreBuildHook(Protocol):
    """Called before build starts. Can modify context."""
    def __call__(self, context: IterationContext) -> IterationContext: ...


class PostCubeLoadHook(Protocol):
    """Called after each cube is loaded. Can modify content."""
    def __call__(self, cube: PromptCube, content: str) -> str: ...


class PostTemplateHook(Protocol):
    """Called after template substitution. Can modify rendered content."""
    def __call__(self, content: str, target: str) -> str: ...


class PostBuildHook(Protocol):
    """Called after build completes. Can modify bundle."""
    def __call__(self, bundle: PromptBundle) -> PromptBundle: ...


# === Hook Runner ===

class HookRunner:
    """Executes hooks with graceful error handling."""

    def __init__(
        self,
        hooks: Optional[Dict[str, List[Callable[..., Any]]]] = None,
        fail_on_error: bool = False
    ):
        """Initialize hook runner.

        Args:
            hooks: Dict mapping hook type to list of hook functions
            fail_on_error: If True, raise exceptions. If False, log and continue.
        """
        self.hooks = hooks or {}
        self.fail_on_error = fail_on_error

    def run_pre_build(self, context: IterationContext) -> IterationContext:
        """Run pre_build hooks."""
        for hook in self.hooks.get("pre_build", []):
            try:
                context = hook(context)
            except Exception as e:
                self._handle_error("pre_build", hook, e)
        return context

    def run_post_cube_load(self, cube: PromptCube, content: str) -> str:
        """Run post_cube_load hooks."""
        for hook in self.hooks.get("post_cube_load", []):
            try:
                content = hook(cube, content)
            except Exception as e:
                self._handle_error("post_cube_load", hook, e)
        return content

    def run_post_template(self, content: str, target: str) -> str:
        """Run post_template hooks."""
        for hook in self.hooks.get("post_template", []):
            try:
                content = hook(content, target)
            except Exception as e:
                self._handle_error("post_template", hook, e)
        return content

    def run_post_build(self, bundle: PromptBundle) -> PromptBundle:
        """Run post_build hooks."""
        for hook in self.hooks.get("post_build", []):
            try:
                bundle = hook(bundle)
            except Exception as e:
                self._handle_error("post_build", hook, e)
        return bundle

    def _handle_error(self, hook_type: str, hook: Callable[..., Any], error: Exception) -> None:
        """Handle hook errors - log and optionally raise."""
        hook_name = getattr(hook, "__name__", str(hook))
        logger.error(f"[HookRunner] Error in {hook_type}/{hook_name}: {error}")
        if self.fail_on_error:
            raise HookError(f"Hook {hook_type}/{hook_name} failed: {error}") from error

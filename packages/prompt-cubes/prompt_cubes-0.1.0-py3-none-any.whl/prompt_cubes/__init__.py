"""
Prompt Cubes SDK - LEGO Constructor for LLM prompts.

Modular YAML-based prompt assembly with matrix configuration.

Script: __init__.py
Created: 2026-01-13
Purpose: Public API exports
Keywords: prompt-cubes, sdk, prompts, llm
Status: active

Example usage:
    from prompt_cubes import PromptService, IterationContext

    service = PromptService(cubes_path="./my-cubes")
    context = IterationContext(
        mode="chatbot",
        agent_type="default",
        iteration=1,
        max_iterations=3,
        user_query="Hello!"
    )
    bundle = service.build(context)
    print(bundle.system_prompt)
"""

from .models import (
    PromptCube,
    ModelConfig,
    IterationContext,
    PromptBundle,
)
from .loader import YAMLLoader
from .service import PromptService
from .hooks import (
    HookRunner,
    PreBuildHook,
    PostCubeLoadHook,
    PostTemplateHook,
    PostBuildHook,
)
from .adapters import (
    SchemaAdapter,
    GeminiAdapter,
    OpenAIAdapter,
    AnthropicAdapter,
    get_adapter,
)
from .exceptions import (
    PromptCubesError,
    CubeLoadError,
    CubeNotFoundError,
    MatrixConfigError,
    HookError,
)

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "PromptCube",
    "ModelConfig",
    "IterationContext",
    "PromptBundle",
    # Core
    "YAMLLoader",
    "PromptService",
    # Hooks
    "HookRunner",
    "PreBuildHook",
    "PostCubeLoadHook",
    "PostTemplateHook",
    "PostBuildHook",
    # Adapters
    "SchemaAdapter",
    "GeminiAdapter",
    "OpenAIAdapter",
    "AnthropicAdapter",
    "get_adapter",
    # Exceptions
    "PromptCubesError",
    "CubeLoadError",
    "CubeNotFoundError",
    "MatrixConfigError",
    "HookError",
]

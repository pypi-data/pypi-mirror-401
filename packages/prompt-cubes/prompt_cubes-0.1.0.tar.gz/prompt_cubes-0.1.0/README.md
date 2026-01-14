# Prompt Cubes SDK

**LEGO Constructor for LLM prompts** - Modular YAML-based prompt assembly with matrix configuration.

## Overview

Prompt Cubes is a Python SDK for building modular, configurable prompts for Large Language Models. It uses a "LEGO blocks" approach where prompt fragments (cubes) are defined in YAML files and assembled based on a configuration matrix.

### Key Features

- **Modular Design**: Build prompts from reusable YAML "cubes"
- **Matrix Configuration**: Combine cubes based on mode/agent/iteration
- **Inline JSON Schema**: Define response schemas directly in cubes
- **Hooks Pipeline**: Customize prompt assembly with pre/post hooks
- **Multi-Provider**: Adapters for Gemini, OpenAI, and Anthropic
- **Hot-Reload**: Reload cubes without restarting
- **Type-Safe**: Full type hints for IDE support

## Installation

```bash
# From local path
pip install -e /path/to/prompt-cubes

# From git (when published)
pip install git+https://github.com/user/prompt-cubes.git
```

## Quick Start

```python
from prompt_cubes import PromptService, IterationContext

# Initialize service with your cubes directory
service = PromptService(cubes_path="./my-cubes")

# Create context for prompt assembly
context = IterationContext(
    mode="chatbot",
    agent_type="default",
    iteration=1,
    max_iterations=3,
    user_query="What is Python?",
    datetime_context="2026-01-13 15:30"
)

# Build the prompt
bundle = service.build(context)

# Access the assembled prompts
print(bundle.system_prompt)
print(bundle.user_prompt)
print(bundle.response_schema)

# Get LLM-ready config
llm_config = bundle.to_llm_config()
```

## Directory Structure

Your cubes directory should follow this structure:

```
my-cubes/
├── cubes/
│   ├── roles/           # Role definitions (e.g., chatbot.yaml)
│   ├── context/         # Context cubes (e.g., session.yaml)
│   ├── modes/           # Mode modifiers (e.g., concise.yaml)
│   ├── user/            # User prompt cubes (e.g., query.yaml)
│   └── tools/           # Tool definitions
└── configs/
    ├── cube_matrix.yaml  # Assembly matrix
    └── models.yaml       # Model configurations
```

## Core Concepts

### Cubes

A cube is a YAML file containing a prompt fragment:

```yaml
id: ROLE_CHATBOT
target: system          # system | user
priority: 1             # Lower = earlier in prompt
category: roles
template: false         # Enable {{variable}} substitution

content: |
  You are a helpful assistant.

schema:                 # Inline JSON schema (merged into response_schema)
  response:
    type: string
    required: true
    description: "Your response to the user"
```

### Matrix Configuration

The `cube_matrix.yaml` defines which cubes combine for each mode/agent/iteration:

```yaml
chatbot:                    # Role/mode
  default:                  # Agent type
    iteration_any:          # Iteration key
      system:
        - ROLE_CHATBOT
        - CONTEXT_SESSION
      user:
        - USER_QUERY

  concise:
    iteration_any:
      system:
        - ROLE_CHATBOT
        - CONTEXT_SESSION
        - MODE_CONCISE
      user:
        - USER_QUERY
```

### Template Variables

Cubes with `template: true` support variable substitution:

- `{{variable}}` - Replaced by IterationContext fields
- `{variable}` - Legacy single-brace syntax

Built-in variables:
- `{{user_query}}`, `{{conversation_history}}`
- `{{datetime_context}}`, `{{user_info}}`
- `{{agent_iteration}}`, `{{agent_max_iterations}}`
- `{{session_turn}}`, `{{session_max_turns}}`
- Custom variables via `context.template_vars`

### Hooks Pipeline

Customize prompt assembly with hooks:

```python
def log_context(context: IterationContext) -> IterationContext:
    print(f"Building for mode: {context.mode}")
    return context

def validate_schema(bundle: PromptBundle) -> PromptBundle:
    assert bundle.response_schema.get("properties")
    return bundle

service = PromptService(
    cubes_path="./cubes",
    hooks={
        "pre_build": [log_context],
        "post_build": [validate_schema]
    }
)
```

Hook types:
- `pre_build`: Before assembly starts
- `post_cube_load`: After each cube is loaded
- `post_template`: After template substitution
- `post_build`: After bundle is complete

### Schema Adapters

Convert schemas for different LLM providers:

```python
from prompt_cubes import get_adapter

# Build prompt
bundle = service.build(context)

# Adapt schema for OpenAI
openai_adapter = get_adapter("openai")
openai_schema = openai_adapter.adapt(bundle.response_schema)

# Use with OpenAI API
tools = [openai_schema]
```

Supported providers:
- `gemini` - Gemini response_schema (default/passthrough)
- `openai` - OpenAI function calling with strict mode
- `anthropic` - Anthropic tool use format

## API Reference

### PromptService

```python
class PromptService:
    def __init__(
        self,
        cubes_path: str = None,
        hooks: Dict[str, List[Callable]] = None,
        search_presets: Dict[str, Any] = None,
        fail_on_hook_error: bool = False
    ): ...

    def build(self, context: IterationContext) -> PromptBundle: ...
    def reload(self) -> None: ...
    def list_cubes(self) -> List[str]: ...
    def get_cube_content(self, cube_id: str) -> Optional[str]: ...

    @classmethod
    def from_config(cls, config_path: str) -> "PromptService": ...
```

### IterationContext

```python
@dataclass
class IterationContext:
    mode: str               # e.g., "chatbot", "assistant"
    agent_type: str         # e.g., "default", "concise"
    iteration: int          # Current iteration (1-based)
    max_iterations: int     # Maximum iterations allowed

    # Session
    session_turn: int = 1
    session_max_turns: int = 10

    # User data
    user_query: str = ""
    conversation_history: str = ""
    datetime_context: str = ""

    # Custom variables
    template_vars: Dict[str, Any] = field(default_factory=dict)
    search_presets: Optional[Dict[str, Any]] = None
```

### PromptBundle

```python
@dataclass
class PromptBundle:
    system_prompt: str
    user_prompt: str
    model_config: ModelConfig
    response_schema: Dict[str, Any]
    dump_info: Dict[str, Any]

    def to_llm_config(self) -> Dict[str, Any]: ...
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Type checking
mypy prompt_cubes/

# Linting
ruff check prompt_cubes/
```

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or PR.

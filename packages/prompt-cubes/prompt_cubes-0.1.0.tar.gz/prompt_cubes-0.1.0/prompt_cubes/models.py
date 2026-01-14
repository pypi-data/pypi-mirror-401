"""
Data models for prompt-cubes SDK.

Script: models.py
Created: 2026-01-13
Purpose: Core dataclasses for prompt assembly
Keywords: models, dataclasses, prompt, cube
Status: active
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel


@dataclass
class PromptCube:
    """A single prompt cube loaded from YAML (LEGO-style building block)."""
    id: str
    target: str  # system | user | schema
    priority: int
    category: str
    content: Optional[str] = None
    template: bool = False
    description: Optional[str] = None
    model_config: Optional[Dict[str, Any]] = None
    schema: Optional[Dict[str, Any]] = None  # Inline schema for this cube
    fragments: Optional[Dict[str, Any]] = None  # Legacy: For separate schema files


@dataclass
class ModelConfig:
    """LLM model configuration."""
    provider: str = "google"
    model_name: str = "gemini-2.5-pro"
    temperature: float = 0.9
    top_p: float = 0.95
    top_k: int = 64
    max_output_tokens: int = 65536
    response_mime_type: str = "application/json"


@dataclass
class IterationContext:
    """Context for prompt assembly."""
    # Core identifiers
    mode: str  # "assistant" | "navigator" | custom
    agent_type: str  # "agent1" | "agent2" | "default"
    iteration: int
    max_iterations: int

    # Session state
    session_turn: int = 1
    session_max_turns: int = 10

    # User prompt data
    datetime_context: str = ""
    user_info: str = ""
    user_query: str = ""
    intent_analysis: str = ""
    conversation_history: str = ""

    # Materials & knowledge
    materials_count: int = 0
    accumulated_knowledge: str = ""
    compact_materials: str = ""
    previous_handover: str = ""

    # Action results
    pending_results_status: str = ""
    user_clarification: str = ""

    # Raw data for advanced processing
    found_materials: List[Dict[str, Any]] = field(default_factory=list)
    previous_handover_dict: Optional[Dict[str, Any]] = None

    # Additional template variables
    template_vars: Dict[str, Any] = field(default_factory=dict)

    # NEW: Injectable search presets (removes MODE_CONFIG dependency)
    search_presets: Optional[Dict[str, Any]] = None


@dataclass
class PromptBundle:
    """Complete prompt bundle ready for LLM call."""
    system_prompt: str
    user_prompt: str
    model_config: ModelConfig
    response_schema: Dict[str, Any]
    dump_info: Dict[str, Any]

    # Optional Pydantic validator
    validator: Optional[Any] = None  # Optional[Type[BaseModel]]

    def to_llm_config(self) -> Dict[str, Any]:
        """Convert to generation_config dict for LLM APIs.

        Returns dict with:
        - model: model name (e.g. 'models/gemini-2.5-pro')
        - system_instruction: system prompt text
        - temperature, top_p, top_k, max_output_tokens: model params
        - response_mime_type: 'application/json'
        - response_schema: JSON Schema for structured output
        """
        # Ensure model name has 'models/' prefix for Gemini
        model_name = self.model_config.model_name
        if not model_name.startswith('models/'):
            model_name = f'models/{model_name}'

        return {
            'model': model_name,
            'system_instruction': self.system_prompt,
            'temperature': self.model_config.temperature,
            'top_p': self.model_config.top_p,
            'top_k': self.model_config.top_k,
            'max_output_tokens': self.model_config.max_output_tokens,
            'response_mime_type': self.model_config.response_mime_type,
            'response_schema': self.response_schema
        }

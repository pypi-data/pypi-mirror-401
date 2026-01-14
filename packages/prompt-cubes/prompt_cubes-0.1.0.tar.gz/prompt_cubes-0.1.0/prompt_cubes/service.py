"""
PromptService - LEGO Constructor for assembling prompts from YAML cubes.

Script: service.py
Created: 2026-01-13
Purpose: Main prompt assembly service with hooks support
Keywords: prompts, service, assembly, lego, cubes
Status: active
"""

from typing import Dict, Any, List, Optional, Callable
import logging
import re

from .models import PromptCube, ModelConfig, IterationContext, PromptBundle
from .loader import YAMLLoader
from .hooks import HookRunner

logger = logging.getLogger(__name__)


class PromptService:
    """
    LEGO Constructor for prompts.

    Loads YAML cubes and assembles them based on:
    - Mode (assistant, navigator, chatbot, etc.)
    - Agent type (agent1, agent2, default, etc.)
    - Iteration number

    Example:
        service = PromptService(cubes_path="./cubes")
        context = IterationContext(
            mode="chatbot",
            agent_type="default",
            iteration=1,
            max_iterations=3
        )
        bundle = service.build(context)
        # bundle.system_prompt, bundle.user_prompt, bundle.response_schema
    """

    def __init__(
        self,
        cubes_path: Optional[str] = None,
        hooks: Optional[Dict[str, List[Callable[..., Any]]]] = None,
        search_presets: Optional[Dict[str, Any]] = None,
        fail_on_hook_error: bool = False
    ):
        """Initialize PromptService.

        Args:
            cubes_path: Path to directory containing cubes/ and configs/
            hooks: Dict of hook functions keyed by hook type
            search_presets: Default search presets config (injectable)
            fail_on_hook_error: If True, hook errors raise exceptions
        """
        self.loader = YAMLLoader(cubes_path)
        self.loader.load_all()
        self.hook_runner = HookRunner(hooks=hooks, fail_on_error=fail_on_hook_error)
        self._search_presets = search_presets or {}

    @classmethod
    def from_config(cls, config_path: str, **kwargs: Any) -> "PromptService":
        """Create PromptService from a configuration file path.

        Args:
            config_path: Path to directory with cubes/ and configs/
            **kwargs: Additional arguments passed to __init__
        """
        return cls(cubes_path=config_path, **kwargs)

    def build(self, context: IterationContext) -> PromptBundle:
        """Build a complete prompt bundle for the given context.

        Args:
            context: IterationContext with mode, agent_type, iteration, etc.

        Returns:
            PromptBundle with system_prompt, user_prompt, model_config, response_schema
        """
        # 0. Run pre_build hooks
        context = self.hook_runner.run_pre_build(context)

        # 1. Get iteration key
        iter_key = self._get_iteration_key(context.iteration)
        logger.info(f"[PromptService] Building: mode={context.mode}, agent={context.agent_type}, iter={iter_key}")

        # 2. Get cube lists from matrix
        cube_lists = self._get_cube_lists(context.mode, context.agent_type, iter_key)
        logger.debug(f"[PromptService] Cubes: system={cube_lists.get('system', [])}, user={cube_lists.get('user', [])}")

        # 3. Load model config
        model_config = self._get_model_config(context.mode, context.agent_type)

        # 4. Assemble system prompt
        system_prompt = self._assemble_prompt(
            cube_lists.get('system', []),
            context,
            target='system'
        )

        # 5. Assemble user prompt
        user_prompt = self._assemble_prompt(
            cube_lists.get('user', []),
            context,
            target='user'
        )

        # 6. Assemble response schema from ALL cubes
        all_cube_ids = (
            cube_lists.get('system', []) +
            cube_lists.get('user', []) +
            cube_lists.get('schema', [])  # Legacy: separate schema cubes
        )
        response_schema = self._assemble_schema(all_cube_ids)

        # 7. Build dump info
        dump_info = {
            "mode": context.mode,
            "agent_type": context.agent_type,
            "iteration": context.iteration,
            "iter_key": iter_key,
            "model": model_config.model_name,
            "provider": model_config.provider,
            "temperature": model_config.temperature,
            "cubes": cube_lists,
            "system_prompt_length": len(system_prompt),
            "user_prompt_length": len(user_prompt),
        }

        bundle = PromptBundle(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_config=model_config,
            response_schema=response_schema,
            dump_info=dump_info
        )

        # 8. Run post_build hooks
        bundle = self.hook_runner.run_post_build(bundle)

        return bundle

    def _get_iteration_key(self, iteration: int) -> str:
        """Determine iteration key for matrix lookup."""
        if iteration == 1:
            return "iteration_1"
        else:
            return "iteration_2_plus"

    def _get_cube_lists(
        self,
        mode: str,
        agent_type: str,
        iter_key: str
    ) -> Dict[str, List[str]]:
        """Get cube ID lists from matrix."""
        matrix = self.loader.get_matrix()

        # Navigate: mode → agent_type → iteration_key
        mode_config = matrix.get(mode, {})
        agent_config = mode_config.get(agent_type, {})

        # Try iteration-specific, then iteration_any
        if iter_key in agent_config:
            return agent_config[iter_key]
        elif "iteration_any" in agent_config:
            return agent_config["iteration_any"]
        else:
            logger.warning(f"[PromptService] No cube config for {mode}/{agent_type}/{iter_key}")
            return {"system": [], "user": [], "schema": []}

    def _get_model_config(self, mode: str, agent_type: str) -> ModelConfig:
        """Get model configuration for mode/agent."""
        config_dict = self.loader.get_model_config(mode, agent_type)

        # Try to get from role cube
        role_id = f"ROLE_{mode.upper()}"
        role_cube = self.loader.get_cube(role_id)
        if role_cube and role_cube.model_config:
            config_dict.update(role_cube.model_config)

        return ModelConfig(
            provider=config_dict.get('provider', 'google'),
            model_name=config_dict.get('model_name', 'gemini-2.5-pro'),
            temperature=config_dict.get('temperature', 0.9),
            top_p=config_dict.get('top_p', 0.95),
            top_k=config_dict.get('top_k', 64),
            max_output_tokens=config_dict.get('max_output_tokens', 65536)
        )

    def _assemble_prompt(
        self,
        cube_ids: List[str],
        context: IterationContext,
        target: str
    ) -> str:
        """Assemble prompt from cubes."""
        cubes = self.loader.get_cubes(cube_ids)
        parts = []

        for cube in cubes:
            if cube.content:
                content = cube.content

                # Run post_cube_load hooks
                content = self.hook_runner.run_post_cube_load(cube, content)

                # Apply template if needed
                if cube.template:
                    content = self._apply_template(content, context)

                # Run post_template hooks
                content = self.hook_runner.run_post_template(content, target)

                parts.append(content)

        return "\n\n".join(parts)

    def _assemble_schema(self, all_cube_ids: List[str]) -> Dict[str, Any]:
        """Assemble JSON Schema from cubes with inline schemas."""
        properties: Dict[str, Any] = {}
        required: List[str] = []

        for cube_id in all_cube_ids:
            cube = self.loader.get_cube(cube_id)
            if not cube:
                continue

            # Check for inline schema in cube
            if cube.schema:
                for prop_name, prop_def in cube.schema.items():
                    if not isinstance(prop_def, dict):
                        continue

                    # Extract required flag
                    is_required = prop_def.get('required', False)

                    # Copy without 'required' field
                    prop_copy = {k: v for k, v in prop_def.items() if k != 'required'}
                    properties[prop_name] = prop_copy

                    if is_required:
                        required.append(prop_name)

            # Legacy: check fragments
            if cube.fragments:
                for frag_id, frag_data in cube.fragments.items():
                    schema_part = frag_data.get('schema', {})
                    properties.update(schema_part)

                    if frag_data.get('required', False):
                        required.extend(schema_part.keys())

        return {
            "type": "object",
            "properties": properties,
            "required": list(set(required))
        }

    def _apply_template(self, content: str, context: IterationContext) -> str:
        """Apply template variables to content.

        Variable syntax:
        - {{variable}} = Template variables (replaced by service)
        - {variable} = Legacy single-brace (backwards compatibility)
        - <<@variable>> = Cognitive variables for LLM reasoning (NOT replaced)
        """
        # Generate dynamic search presets content
        presets_table, temporal_scopes, limits = self._format_search_presets(context)

        template_vars = {
            # System prompt variables
            "agent_iteration": context.iteration,
            "agent_max_iterations": context.max_iterations,
            "session_turn": context.session_turn,
            "session_max_turns": context.session_max_turns,
            "kept_materials_count": context.materials_count,
            "accumulated_knowledge_summary": context.accumulated_knowledge or "First iteration.",

            # User prompt variables
            "datetime_context": context.datetime_context or "(not specified)",
            "user_info": context.user_info or "(unknown user)",
            "user_query": context.user_query or "(no query)",
            "intent_analysis": context.intent_analysis or "(no analysis)",
            "conversation_history": context.conversation_history or "(no history)",
            "accumulated_knowledge": context.accumulated_knowledge or "(first iteration)",
            "compact_materials": context.compact_materials or "(no materials found)",
            "materials_count": context.materials_count,
            "previous_handover": context.previous_handover or "(no notes)",
            "pending_results_status": context.pending_results_status or "",
            "user_clarification": context.user_clarification or "",

            # Dynamic search presets
            "PRESETS_TABLE": presets_table,
            "TEMPORAL_SCOPES": temporal_scopes,
            "LIMITS": limits,

            # Additional vars from template_vars dict
            **context.template_vars
        }

        def replace_var(match: re.Match[str]) -> str:
            var_name = match.group(1).strip()
            if var_name in template_vars:
                return str(template_vars[var_name])
            logger.warning(f"[PromptService] Missing template variable: {var_name}")
            return match.group(0)  # Keep original if not found

        # Replace {{variable}} (double braces)
        content = re.sub(r'\{\{([^}]+)\}\}', replace_var, content)
        # Replace {variable} (single braces) - backwards compatibility
        content = re.sub(r'\{([a-z_]+)\}', replace_var, content)
        return content

    def _format_search_presets(self, context: IterationContext) -> tuple[str, str, str]:
        """Format search presets for prompt injection.

        Uses presets from:
        1. context.search_presets (highest priority)
        2. self._search_presets (service-level default)
        3. Empty defaults
        """
        presets_config = (
            context.search_presets or
            self._search_presets.get(context.mode, {}) or
            {}
        )
        search_presets = presets_config.get('search_presets', {})
        search_limits = presets_config.get('search_limits', {})
        temporal_scopes = presets_config.get('temporal_scopes', {})

        # Format presets table
        if search_presets:
            presets_lines = ["| Preset | Description | Detail | Limit | Scope |",
                            "|--------|-------------|--------|-------|-------|"]
            for name, preset in search_presets.items():
                desc = preset.get('description', '')[:50]
                detail = preset.get('detail_level', 'brief')
                limit = preset.get('limit', 10)
                scope = preset.get('temporal_scope') or 'all_time'
                presets_lines.append(f"| `{name}` | {desc} | {detail} | {limit} | {scope} |")
            presets_table = "\n".join(presets_lines)
        else:
            presets_table = "(no presets configured)"

        # Format temporal scopes
        if temporal_scopes:
            scopes_lines = []
            for name, cfg in temporal_scopes.items():
                if cfg is None:
                    scopes_lines.append(f"- `{name}`: no restrictions")
                else:
                    days = cfg.get('days', 30)
                    mode_str = cfg.get('mode', 'soft')
                    scopes_lines.append(f"- `{name}`: last {days} days ({mode_str})")
            temporal_scopes_str = "\n".join(scopes_lines)
        else:
            temporal_scopes_str = "(no scopes configured)"

        # Format limits
        if search_limits:
            limits_lines = [
                f"- **headers**: max {search_limits.get('headers_max', 100)} items",
                f"- **brief/full**: max {search_limits.get('hard_max', 50)} items",
                f"- **deep**: max {search_limits.get('deep_max', 10)} items"
            ]
            limits_str = "\n".join(limits_lines)
        else:
            limits_str = "(no limits configured)"

        return presets_table, temporal_scopes_str, limits_str

    def reload(self) -> None:
        """Reload all cubes and configs (hot-reload)."""
        self.loader.reload()

    def list_cubes(self) -> List[str]:
        """List all available cube IDs."""
        return self.loader.list_cubes()

    def get_cube_content(self, cube_id: str) -> Optional[str]:
        """Get content of a specific cube."""
        cube = self.loader.get_cube(cube_id)
        return cube.content if cube else None

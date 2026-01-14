"""
YAML loader for prompt cubes with caching and hot-reload support.

Script: loader.py
Created: 2026-01-13
Purpose: Load and cache YAML prompt cubes
Keywords: yaml, loader, cubes, cache, prompts
Status: active
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

from .models import PromptCube
from .exceptions import CubeLoadError

logger = logging.getLogger(__name__)


class YAMLLoader:
    """
    Loads and caches YAML prompt cubes.

    Directory structure:
    {base_path}/
    ├── cubes/
    │   ├── roles/
    │   ├── tools/
    │   ├── context/
    │   ├── formatting/
    │   ├── modes/
    │   └── user/
    └── configs/
        ├── cube_matrix.yaml
        └── models.yaml
    """

    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            # Default to current directory
            base_path = Path.cwd()
        self.base_path = Path(base_path)
        self.cubes_path = self.base_path / "cubes"
        self.configs_path = self.base_path / "configs"

        # Cache
        self._cubes: Dict[str, PromptCube] = {}
        self._matrix: Dict[str, Any] = {}
        self._models: Dict[str, Any] = {}
        self._loaded = False

    def load_all(self, force_reload: bool = False) -> None:
        """Load all cubes and configs."""
        if self._loaded and not force_reload:
            return

        self._load_cubes()
        self._load_matrix()
        self._load_models()
        self._loaded = True

        logger.info(f"[YAMLLoader] Loaded {len(self._cubes)} prompt cubes from {self.cubes_path}")

    def reload(self) -> None:
        """Force reload all cubes and configs (hot-reload)."""
        self._loaded = False
        self._cubes = {}
        self._matrix = {}
        self._models = {}
        self.load_all(force_reload=True)

    def _load_cubes(self) -> None:
        """Load all cube YAML files from cubes/ directory."""
        self._cubes = {}

        if not self.cubes_path.exists():
            logger.warning(f"[YAMLLoader] Cubes path not found: {self.cubes_path}")
            return

        for yaml_file in self.cubes_path.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if not data:
                    continue

                # Handle schema files with multiple fragments (legacy)
                if 'fragments' in data:
                    for frag_id, frag_data in data['fragments'].items():
                        cube = PromptCube(
                            id=frag_id,
                            target='schema',
                            priority=data.get('priority', 50),
                            category='schema',
                            fragments={frag_id: frag_data}
                        )
                        self._cubes[frag_id] = cube
                else:
                    # Regular cube (may have inline schema)
                    cube = PromptCube(
                        id=data.get('id', yaml_file.stem),
                        target=data.get('target', 'system'),
                        priority=data.get('priority', 50),
                        category=data.get('category', 'general'),
                        content=data.get('content'),
                        template=data.get('template', False),
                        description=data.get('description'),
                        model_config=data.get('model_config'),
                        schema=data.get('schema')  # Inline schema
                    )
                    self._cubes[cube.id] = cube

            except Exception as e:
                logger.error(f"[YAMLLoader] Failed to load {yaml_file}: {e}")

    def _load_matrix(self) -> None:
        """Load cube_matrix.yaml."""
        matrix_file = self.configs_path / "cube_matrix.yaml"
        if matrix_file.exists():
            with open(matrix_file, 'r', encoding='utf-8') as f:
                self._matrix = yaml.safe_load(f) or {}
            # Log loaded modes
            for mode in self._matrix:
                agents = self._matrix.get(mode, {})
                for agent, iters in agents.items():
                    iter_keys = list(iters.keys()) if isinstance(iters, dict) else []
                    logger.debug(f"[YAMLLoader] Matrix: {mode}/{agent} → {iter_keys}")
        else:
            logger.warning(f"[YAMLLoader] Matrix config not found: {matrix_file}")

    def _load_models(self) -> None:
        """Load models.yaml."""
        models_file = self.configs_path / "models.yaml"
        if models_file.exists():
            with open(models_file, 'r', encoding='utf-8') as f:
                self._models = yaml.safe_load(f) or {}
        else:
            logger.warning(f"[YAMLLoader] Models config not found: {models_file}")

    def get_cube(self, cube_id: str) -> Optional[PromptCube]:
        """Get a single cube by ID."""
        self.load_all()
        return self._cubes.get(cube_id)

    def get_cubes(self, cube_ids: List[str]) -> List[PromptCube]:
        """Get multiple cubes, sorted by priority."""
        self.load_all()
        cubes = [self._cubes[cid] for cid in cube_ids if cid in self._cubes]
        return sorted(cubes, key=lambda c: c.priority)

    def get_matrix(self) -> Dict[str, Any]:
        """Get the cube assembly matrix."""
        self.load_all()
        return self._matrix

    def get_model_config(self, mode: str, agent: str) -> Dict[str, Any]:
        """Get model config for mode/agent combination.

        Supports two config structures:
        - mode_models.{mode}.{agent}: model_name → looks up in models
        - role_models.{role}.{mode}: model_name → looks up in models
        """
        self.load_all()

        # Try mode_models first (legacy format)
        mode_models = self._models.get('mode_models', {})
        model_name = mode_models.get(mode, {}).get(agent)

        # Try role_models second (new format: role.mode → model)
        if not model_name:
            role_models = self._models.get('role_models', {})
            model_name = role_models.get(mode, {}).get(agent)

        if model_name:
            config = self._models.get('models', {}).get(model_name, {}).copy()
            config['model_name'] = model_name
            return config
        return {}

    def list_cubes(self) -> List[str]:
        """List all loaded cube IDs."""
        self.load_all()
        return list(self._cubes.keys())

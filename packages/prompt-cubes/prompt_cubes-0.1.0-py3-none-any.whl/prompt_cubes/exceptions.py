"""
Custom exceptions for prompt-cubes SDK.

Script: exceptions.py
Created: 2026-01-13
Purpose: SDK-specific exception hierarchy
Keywords: exceptions, errors, prompt-cubes
Status: active
"""


class PromptCubesError(Exception):
    """Base exception for prompt-cubes."""
    pass


class CubeLoadError(PromptCubesError):
    """Failed to load a cube from YAML."""
    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to load cube from {path}: {reason}")


class CubeNotFoundError(PromptCubesError):
    """Cube ID not found in registry."""
    def __init__(self, cube_id: str):
        self.cube_id = cube_id
        super().__init__(f"Cube not found: {cube_id}")


class MatrixConfigError(PromptCubesError):
    """Error in cube_matrix.yaml configuration."""
    pass


class HookError(PromptCubesError):
    """Error in hook execution (logged but not raised by default)."""
    pass

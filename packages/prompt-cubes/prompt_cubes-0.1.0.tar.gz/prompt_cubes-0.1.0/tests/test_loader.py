"""Tests for YAMLLoader."""

import pytest
from prompt_cubes import YAMLLoader


class TestYAMLLoader:
    """Test YAMLLoader functionality."""

    def test_load_cubes_from_examples(self, examples_path):
        """Test loading cubes from examples directory."""
        loader = YAMLLoader(str(examples_path))
        loader.load_all()

        cubes = loader.list_cubes()
        assert len(cubes) >= 4  # At least: ROLE_CHATBOT, CONTEXT_SESSION, USER_QUERY, MODE_CONCISE
        assert "ROLE_CHATBOT" in cubes
        assert "CONTEXT_SESSION" in cubes
        assert "USER_QUERY" in cubes

    def test_get_cube_by_id(self, examples_path):
        """Test getting a specific cube by ID."""
        loader = YAMLLoader(str(examples_path))

        cube = loader.get_cube("ROLE_CHATBOT")
        assert cube is not None
        assert cube.id == "ROLE_CHATBOT"
        assert cube.target == "system"
        assert cube.category == "roles"
        assert cube.content is not None
        assert "helpful" in cube.content.lower()

    def test_get_cubes_sorted_by_priority(self, examples_path):
        """Test that get_cubes returns cubes sorted by priority."""
        loader = YAMLLoader(str(examples_path))

        cubes = loader.get_cubes(["CONTEXT_SESSION", "ROLE_CHATBOT"])
        assert len(cubes) == 2
        # ROLE_CHATBOT has priority 1, CONTEXT_SESSION has priority 10
        assert cubes[0].id == "ROLE_CHATBOT"
        assert cubes[1].id == "CONTEXT_SESSION"

    def test_get_matrix(self, examples_path):
        """Test loading cube matrix."""
        loader = YAMLLoader(str(examples_path))

        matrix = loader.get_matrix()
        assert "chatbot" in matrix
        assert "default" in matrix["chatbot"]
        assert "iteration_any" in matrix["chatbot"]["default"]
        assert "system" in matrix["chatbot"]["default"]["iteration_any"]

    def test_get_model_config(self, examples_path):
        """Test getting model configuration."""
        loader = YAMLLoader(str(examples_path))

        config = loader.get_model_config("chatbot", "default")
        assert config.get("model_name") == "gpt-4o"

    def test_reload(self, examples_path):
        """Test hot-reload functionality."""
        loader = YAMLLoader(str(examples_path))
        loader.load_all()

        initial_count = len(loader.list_cubes())
        loader.reload()

        assert len(loader.list_cubes()) == initial_count

    def test_nonexistent_cube_returns_none(self, examples_path):
        """Test that nonexistent cube returns None."""
        loader = YAMLLoader(str(examples_path))

        cube = loader.get_cube("NONEXISTENT_CUBE")
        assert cube is None

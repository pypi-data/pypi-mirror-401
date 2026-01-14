"""Pytest fixtures for prompt-cubes tests."""

import pytest
from pathlib import Path


@pytest.fixture
def examples_path():
    """Path to examples directory."""
    return Path(__file__).parent.parent / "examples" / "basic-chatbot"


@pytest.fixture
def basic_context():
    """Basic IterationContext for testing."""
    from prompt_cubes import IterationContext
    return IterationContext(
        mode="chatbot",
        agent_type="default",
        iteration=1,
        max_iterations=3,
        session_turn=1,
        session_max_turns=10,
        datetime_context="2026-01-13 15:30",
        user_query="Hello, how are you?",
        conversation_history="",
    )


@pytest.fixture
def service(examples_path):
    """PromptService instance using example cubes."""
    from prompt_cubes import PromptService
    return PromptService(cubes_path=str(examples_path))

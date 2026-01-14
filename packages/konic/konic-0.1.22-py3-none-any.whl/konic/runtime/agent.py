"""Agent registration for Konic engine discovery."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from konic.common.errors.cli import KonicValidationError

if TYPE_CHECKING:
    from konic.agent import KonicAgent

_REGISTERED_AGENT_INSTANCE: KonicAgent | None = None
_REGISTERED_ENV_CLASS: Any = None


def _is_finetuning_agent(agent_instance: Any) -> bool:
    """Check if agent has get_finetuning_method (finetuning vs RL agent)."""
    return hasattr(agent_instance, "get_finetuning_method") and callable(
        getattr(agent_instance, "get_finetuning_method")
    )


def _perform_registration(agent_instance: KonicAgent, name: str) -> KonicAgent:
    global _REGISTERED_AGENT_INSTANCE, _REGISTERED_ENV_CLASS

    if not name:
        raise KonicValidationError("Agent name is required.")

    if inspect.isclass(agent_instance):
        raise KonicValidationError(
            f"Expected an agent instance, got class {agent_instance.__name__}. "
            "Please instantiate it first."
        )

    env_class = None
    if not _is_finetuning_agent(agent_instance):
        env_class = agent_instance.get_environment()

    try:
        setattr(
            agent_instance,
            "_konic_meta",
            {"name": name, "env_module": env_class},
        )
    except AttributeError as e:
        raise KonicValidationError(f"Failed to set metadata on agent instance: {e}") from e

    _REGISTERED_AGENT_INSTANCE = agent_instance
    _REGISTERED_ENV_CLASS = env_class

    return agent_instance


def register_agent(agent_instance: Any, name: str) -> Any:
    """Register a KonicAgent instance for engine discovery."""
    return _perform_registration(agent_instance, name)


def get_registered_agent() -> tuple[Any, Any]:
    """Get (agent_instance, environment_class) tuple."""
    return _REGISTERED_AGENT_INSTANCE, _REGISTERED_ENV_CLASS

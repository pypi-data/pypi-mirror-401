"""Data dependency registration for Konic agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from konic.common.errors.cli import KonicValidationError

VersionType = str | Literal["latest"]


@dataclass(frozen=True)
class DataDependency:
    """Registered data dependency (cloud_name, env_var, version)."""

    cloud_name: str
    env_var: str
    version: str


_REGISTERED_DATA: list[DataDependency] = []


def register_data(
    cloud_name: str,
    env_var: str,
    version: VersionType = "latest",
) -> DataDependency:
    """Register a dataset dependency to be downloaded at training time."""
    if not cloud_name:
        raise KonicValidationError(
            "Data cloud_name is required.",
            field="cloud_name",
        )

    if not env_var:
        raise KonicValidationError(
            "Data env_var is required.",
            field="env_var",
        )

    normalized_env_var = env_var.upper().replace("-", "_").replace(" ", "_")

    dependency = DataDependency(
        cloud_name=cloud_name,
        env_var=normalized_env_var,
        version=version,
    )

    _REGISTERED_DATA.append(dependency)
    return dependency


def get_registered_data() -> list[DataDependency]:
    """Get all registered data dependencies (used internally by engine)."""
    return _REGISTERED_DATA.copy()


def clear_registered_data() -> None:
    """Clear all registered data dependencies (for testing)."""
    global _REGISTERED_DATA
    _REGISTERED_DATA = []

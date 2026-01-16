"""Backend capability declarations for upfront validation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BackendCapabilities:
    """Declares what a backend supports for upfront validation.

    This allows the engine to validate configuration against backend
    capabilities before training starts, providing clear error messages.
    """

    supports_online_generation: bool = True
    """Whether backend generates responses during training (PPO, GRPO)."""

    supports_offline_preference: bool = False
    """Whether backend learns from preference pairs (DPO)."""

    requires_reward_composer: bool = True
    """Whether a reward composer must be provided."""

    requires_value_head: bool = True
    """Whether backend needs a value model (PPO) or not (GRPO, DPO)."""

    supports_lora: bool = True
    """Whether LoRA adapters are supported."""

    supports_gradient_accumulation: bool = True
    """Whether gradient accumulation is supported."""

    supports_amp: bool = True
    """Whether automatic mixed precision is supported."""


# Predefined capability sets for common backend types
ONLINE_RL_CAPABILITIES = BackendCapabilities(
    supports_online_generation=True,
    supports_offline_preference=False,
    requires_reward_composer=True,
    requires_value_head=True,
)

GRPO_CAPABILITIES = BackendCapabilities(
    supports_online_generation=True,
    supports_offline_preference=False,
    requires_reward_composer=True,
    requires_value_head=False,
)

DPO_CAPABILITIES = BackendCapabilities(
    supports_online_generation=False,
    supports_offline_preference=True,
    requires_reward_composer=False,
    requires_value_head=False,
)

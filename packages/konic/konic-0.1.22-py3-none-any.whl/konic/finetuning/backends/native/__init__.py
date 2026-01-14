"""Native RLHF training backend package.

Provides Konic's custom PPO implementation with fine-grained control
over the training loop, GAE computation, and gradient accumulation.
"""

from konic.finetuning.backends.native.advantage import (
    ADVANTAGE_STD_THRESHOLD,
    compute_gae_advantages,
    normalize_advantages,
)
from konic.finetuning.backends.native.backend import NativeRLHFBackend
from konic.finetuning.backends.native.ppo import PPOUpdater, PPOUpdateResult

__all__ = [
    # Backend
    "NativeRLHFBackend",
    # PPO
    "PPOUpdater",
    "PPOUpdateResult",
    # Advantage computation
    "ADVANTAGE_STD_THRESHOLD",
    "compute_gae_advantages",
    "normalize_advantages",
]

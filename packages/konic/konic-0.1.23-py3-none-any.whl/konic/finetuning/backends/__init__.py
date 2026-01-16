"""Training backends for LLM finetuning.

This module provides pluggable training backends allowing users to choose
between Konic's native implementation and external libraries like TRL.
"""

from konic.finetuning.backends.base import (
    BackendConfig,
    BaseTrainingBackend,
)
from konic.finetuning.backends.capabilities import (
    DPO_CAPABILITIES,
    GRPO_CAPABILITIES,
    ONLINE_RL_CAPABILITIES,
    BackendCapabilities,
)
from konic.finetuning.backends.native import (
    ADVANTAGE_STD_THRESHOLD,
    NativeRLHFBackend,
    PPOUpdater,
    compute_gae_advantages,
)
from konic.finetuning.backends.result import (
    FinetuningIterationResult,
    FinetuningResult,
)

__all__ = [
    # Core
    "BackendConfig",
    "BaseTrainingBackend",
    # Capabilities
    "BackendCapabilities",
    "DPO_CAPABILITIES",
    "GRPO_CAPABILITIES",
    "ONLINE_RL_CAPABILITIES",
    # Native backend
    "ADVANTAGE_STD_THRESHOLD",
    "NativeRLHFBackend",
    "PPOUpdater",
    "compute_gae_advantages",
    # Results
    "FinetuningIterationResult",
    "FinetuningResult",
]

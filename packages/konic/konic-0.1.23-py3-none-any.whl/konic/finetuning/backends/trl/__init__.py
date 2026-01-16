"""TRL backend implementations for LLM finetuning.

This module provides TRL-based training backends for GRPO and DPO methods.
Requires the 'trl' optional dependency: pip install konic[trl]
"""

from konic.finetuning.backends.trl.base import BaseTRLBackend, check_trl_available

__all__ = [
    "BaseTRLBackend",
    "check_trl_available",
]


def get_trl_grpo_backend():
    """Lazy import for GRPO backend."""
    from konic.finetuning.backends.trl.grpo import TRLGRPOBackend

    return TRLGRPOBackend


def get_trl_dpo_backend():
    """Lazy import for DPO backend."""
    from konic.finetuning.backends.trl.dpo import TRLDPOBackend

    return TRLDPOBackend

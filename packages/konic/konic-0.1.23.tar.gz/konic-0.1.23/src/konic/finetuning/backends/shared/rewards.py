"""Shared reward computation utility for finetuning backends."""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING

from konic.common.errors import KonicRuntimeError

if TYPE_CHECKING:
    from konic.finetuning.reward import BaseKonicLLMRewardComposer

logger = logging.getLogger(__name__)


class RewardComputationUtility:
    """Encapsulates prompt+response to reward computation logic.

    Provides a single source of truth for reward computation across backends,
    with fallback from batch to sequential processing.
    """

    def __init__(
        self,
        reward_composer: BaseKonicLLMRewardComposer,
    ) -> None:
        self._composer = reward_composer

    def compute(
        self,
        prompts: list[str],
        responses: list[str],
    ) -> tuple[list[float], dict[str, list[float]]]:
        """Compute rewards for prompt-response pairs.

        Attempts batch computation first, falling back to sequential if
        the composer doesn't support batching.

        Args:
            prompts: List of prompts.
            responses: List of corresponding responses.

        Returns:
            Tuple of (rewards list, breakdown dict mapping reward names to values).
        """
        if hasattr(self._composer, "compose_batch"):
            rewards, breakdowns = self._composer.compose_batch(prompts, responses)
        else:
            rewards, breakdowns = self._compute_sequential(prompts, responses)

        self._validate_rewards(rewards)
        return rewards, breakdowns

    def _validate_rewards(self, rewards: list[float]) -> None:
        """Validate that all rewards are finite values."""
        invalid_indices = [i for i, r in enumerate(rewards) if not math.isfinite(r)]
        if invalid_indices:
            invalid_values = [rewards[i] for i in invalid_indices[:5]]
            raise KonicRuntimeError(
                f"Invalid rewards computed at indices {invalid_indices[:5]}: {invalid_values}. "
                "Check reward functions for division by zero or overflow.",
                operation="reward_computation",
            )

    def _compute_sequential(
        self,
        prompts: list[str],
        responses: list[str],
    ) -> tuple[list[float], dict[str, list[float]]]:
        """Fallback sequential reward computation."""
        rewards = []
        breakdowns: dict[str, list[float]] = {}

        for prompt, response in zip(prompts, responses):
            reward = self._composer.compose(prompt, response)
            rewards.append(reward)

            breakdown = self._composer.get_reward_breakdown(prompt, response)
            for key, value in breakdown.items():
                if key not in breakdowns:
                    breakdowns[key] = []
                breakdowns[key].append(value)

        return rewards, breakdowns

"""Mixins providing shared functionality to finetuning backends."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol

import torch

from konic.finetuning.backends.shared.generation import GenerationOutput, GenerationUtility
from konic.finetuning.backends.shared.rewards import RewardComputationUtility

if TYPE_CHECKING:
    from konic.finetuning.config import GenerationConfig
    from konic.finetuning.reward import BaseKonicLLMRewardComposer


class HasGenerationComponents(Protocol):
    """Protocol for classes that can provide generation components."""

    def _get_model(self) -> Any: ...
    def _get_tokenizer(self) -> Any: ...
    def _get_device(self) -> str: ...
    def _get_generation_config(self) -> GenerationConfig: ...


class HasRewardComposer(Protocol):
    """Protocol for classes that can provide a reward composer."""

    def _get_reward_composer(self) -> BaseKonicLLMRewardComposer: ...


class GenerationMixin:
    """Mixin providing _generate_responses() to backends.

    Requires implementing:
        - _get_model() -> model
        - _get_tokenizer() -> tokenizer
        - _get_device() -> str
        - _get_generation_config() -> GenerationConfig
    """

    @abstractmethod
    def _get_model(self) -> Any:
        """Return the model for generation."""
        pass

    @abstractmethod
    def _get_tokenizer(self) -> Any:
        """Return the tokenizer for generation."""
        pass

    @abstractmethod
    def _get_device(self) -> str:
        """Return the device string (e.g., 'cuda', 'cpu')."""
        pass

    @abstractmethod
    def _get_generation_config(self) -> GenerationConfig:
        """Return the generation configuration."""
        pass

    def _generate_responses(
        self, prompts: list[str]
    ) -> tuple[list[str], torch.Tensor, torch.Tensor]:
        """Generate responses for prompts using shared utility.

        Args:
            prompts: List of input prompts.

        Returns:
            Tuple of (responses, input_ids, response_ids).
        """
        utility = GenerationUtility(
            model=self._get_model(),
            tokenizer=self._get_tokenizer(),
            device=self._get_device(),
            generation_config=self._get_generation_config(),
        )

        output: GenerationOutput = utility.generate(prompts)
        return output.responses, output.input_ids, output.response_ids


class RewardMixin:
    """Mixin providing _compute_rewards() to backends.

    Requires implementing:
        - _get_reward_composer() -> BaseKonicLLMRewardComposer
    """

    @abstractmethod
    def _get_reward_composer(self) -> BaseKonicLLMRewardComposer:
        """Return the reward composer."""
        pass

    def _compute_rewards(
        self,
        prompts: list[str],
        responses: list[str],
    ) -> tuple[list[float], dict[str, list[float]]]:
        """Compute rewards for prompt-response pairs using shared utility.

        Args:
            prompts: List of prompts.
            responses: List of corresponding responses.

        Returns:
            Tuple of (rewards list, reward breakdown dict).
        """
        utility = RewardComputationUtility(
            reward_composer=self._get_reward_composer(),
        )

        return utility.compute(prompts, responses)

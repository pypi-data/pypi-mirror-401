"""Adapt Konic reward composers to TRL reward function signatures."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from konic.finetuning.reward import BaseKonicLLMRewardComposer


def adapt_reward_composer_to_trl(
    composer: BaseKonicLLMRewardComposer,
) -> Callable[[list[str], list[str]], list[float]]:
    """Convert Konic reward composer to TRL reward_funcs signature.

    Konic's @llm_reward methods have signature:
        def reward_method(self, prompt: str, response: str) -> float

    TRL expects:
        def reward_func(completions: list[str], prompts: list[str], **kwargs) -> list[float]
    """

    def trl_reward_func(
        completions: list[str],
        prompts: list[str] | None = None,
        **kwargs,
    ) -> list[float]:
        if prompts is None:
            prompts = kwargs.get("prompt") or [""] * len(completions)

        # Ensure prompts is a list
        prompt_list: list[str] = list(prompts) if prompts else [""] * len(completions)
        rewards, _ = composer.compose_batch(prompt_list, completions)
        return rewards

    return trl_reward_func


def create_reward_func_from_callable(
    reward_fn: Callable[[str, str], float],
) -> Callable[[list[str], list[str]], list[float]]:
    """Create TRL-compatible reward function from a simple callable."""

    def trl_reward_func(
        completions: list[str],
        prompts: list[str] | None = None,
        **kwargs,
    ) -> list[float]:
        if prompts is None:
            prompts = [""] * len(completions)

        return [reward_fn(p, c) for p, c in zip(prompts, completions)]

    return trl_reward_func


def adapt_hf_reward_model(model_name: str):
    """Create TRL-compatible reward function from a HuggingFace reward model.

    TRL can use model IDs directly as reward_funcs.
    """
    return model_name

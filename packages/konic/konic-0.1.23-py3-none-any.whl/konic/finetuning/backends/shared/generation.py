"""Shared generation utility for finetuning backends."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import torch

if TYPE_CHECKING:
    from konic.finetuning.config import GenerationConfig


@dataclass
class GenerationOutput:
    """Output from generation utility."""

    responses: list[str]
    input_ids: torch.Tensor
    response_ids: torch.Tensor


class GenerationUtility:
    """Encapsulates prompt to response generation logic.

    Provides a single source of truth for text generation across backends,
    eliminating duplication between native and TRL implementations.
    """

    def __init__(
        self,
        model: Any,
        tokenizer: Any,
        device: str,
        generation_config: GenerationConfig,
    ) -> None:
        self._model = model
        self._tokenizer = tokenizer
        self._device = device
        self._gen_config = generation_config

    def generate(self, prompts: list[str]) -> GenerationOutput:
        """Generate responses for given prompts.

        Args:
            prompts: List of input prompts.

        Returns:
            GenerationOutput with responses, input_ids, and response_ids tensors.
        """
        inputs = self._tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self._gen_config.max_length,
        )

        input_ids: torch.Tensor = inputs["input_ids"].to(self._device)
        attention_mask: torch.Tensor = inputs["attention_mask"].to(self._device)

        with torch.no_grad():
            output_ids = self._model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=self._gen_config.max_new_tokens,
                do_sample=self._gen_config.do_sample,
                temperature=self._gen_config.temperature,
                top_p=self._gen_config.top_p,
                pad_token_id=self._tokenizer.pad_token_id,
            )

        response_ids = output_ids[:, input_ids.shape[1] :]
        responses = self._tokenizer.batch_decode(response_ids, skip_special_tokens=True)

        return GenerationOutput(
            responses=responses,
            input_ids=input_ids,
            response_ids=response_ids,
        )

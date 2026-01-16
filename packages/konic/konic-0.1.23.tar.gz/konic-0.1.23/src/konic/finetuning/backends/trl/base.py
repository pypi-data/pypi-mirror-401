"""Base class for TRL-based training backends."""

from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Any

from konic.common.errors import KonicConfigurationError
from konic.finetuning.backends.base import BackendConfig, BaseTrainingBackend
from konic.finetuning.backends.result import FinetuningResult

logger = logging.getLogger(__name__)

_TRL_AVAILABLE: bool | None = None


def check_trl_available() -> bool:
    """Check if TRL is installed."""
    global _TRL_AVAILABLE
    if _TRL_AVAILABLE is None:
        try:
            import trl  # noqa: F401

            _TRL_AVAILABLE = True
        except ImportError:
            _TRL_AVAILABLE = False
    return _TRL_AVAILABLE


def require_trl() -> None:
    """Raise error if TRL is not available."""
    if not check_trl_available():
        raise KonicConfigurationError(
            "TRL backend requires the 'trl' package. Install with: pip install konic[trl]",
            config_key="method",
        )


class BaseTRLBackend(BaseTrainingBackend):
    """Abstract base class for TRL-based training backends.

    Provides common functionality for all TRL trainers including model loading,
    MLflow integration, and checkpoint handling.
    """

    def __init__(self) -> None:
        require_trl()
        self._config: BackendConfig | None = None
        self._trainer: Any = None  # TRL Trainer instance
        self._is_setup = False

    @property
    def is_setup(self) -> bool:
        return self._is_setup

    @property
    def config(self) -> BackendConfig:
        if self._config is None:
            raise KonicConfigurationError(
                "Backend not configured. Call setup() first.",
                config_key="backend",
            )
        return self._config

    def setup(self, config: BackendConfig) -> None:
        if self._is_setup:
            return

        self._config = config
        self._validate_config()
        self._create_trainer()
        self._is_setup = True

        logger.info(f"Initialized {self.name} backend for {config.model_name}")

    @abstractmethod
    def _validate_config(self) -> None:
        """Validate method-specific configuration requirements."""
        pass

    @abstractmethod
    def _create_trainer(self) -> None:
        """Create the TRL trainer instance."""
        pass

    @abstractmethod
    def train(self, max_iterations: int, save_every: int | None = None) -> FinetuningResult:
        """Execute training using the TRL trainer."""
        pass

    def evaluate(self, prompts: list[str]) -> dict[str, Any]:
        """Evaluate model on given prompts."""
        if self._trainer is None:
            raise KonicConfigurationError(
                "Trainer not initialized. Call setup() first.",
                config_key="trainer",
            )

        # TRL trainers generate completions via the model
        model = self._trainer.model
        tokenizer = self._trainer.processing_class

        # Switch to evaluation mode for proper generation behavior
        # TRL leaves the model in training mode after train() completes
        was_training = model.training
        model.train(False)

        inputs = tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.config.generation_config.max_length,
        )

        import torch

        with torch.no_grad():
            outputs = model.generate(
                **inputs.to(model.device),
                max_new_tokens=self.config.generation_config.max_new_tokens,
                do_sample=self.config.generation_config.do_sample,
                temperature=self.config.generation_config.temperature,
                top_p=self.config.generation_config.top_p,
            )

        # Decode responses (excluding prompts)
        responses = tokenizer.batch_decode(
            outputs[:, inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )

        # Compute rewards if reward composer is available
        rewards = []
        breakdown: dict[str, list[float]] = {}
        if self.config.reward_composer is not None:
            rewards, breakdown = self.config.reward_composer.compose_batch(prompts, responses)

        # Restore original training mode
        if was_training:
            model.train(True)

        return {
            "prompts": prompts,
            "responses": responses,
            "rewards": rewards,
            "reward_mean": sum(rewards) / len(rewards) if rewards else 0.0,
            "reward_breakdown": breakdown,
        }

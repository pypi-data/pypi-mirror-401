"""Base training backend abstraction for LLM finetuning."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from konic.finetuning.backends.result import FinetuningResult
    from konic.finetuning.callback import BaseKonicFinetuningCallback
    from konic.finetuning.config import GenerationConfig, LoraConfig, TrainingConfig
    from konic.finetuning.dataset import DatasetConfig
    from konic.finetuning.reward import BaseKonicLLMRewardComposer


@dataclass
class BackendConfig:
    """Configuration container passed to training backends."""

    model_name: str
    reward_composer: BaseKonicLLMRewardComposer | None
    dataset_config: DatasetConfig
    lora_config: LoraConfig | None
    training_config: TrainingConfig
    generation_config: GenerationConfig
    callback: BaseKonicFinetuningCallback
    checkpoint_dir: str | None
    device: str


class BaseTrainingBackend(ABC):
    """Abstract base class for training backends.

    Backends implement the actual training logic while KonicFinetuningEngine
    serves as a facade providing a unified API.
    """

    @abstractmethod
    def setup(self, config: BackendConfig) -> None:
        """Initialize backend with configuration.

        Args:
            config: Backend configuration containing model, dataset, and training params.
        """
        pass

    @abstractmethod
    def train(self, max_iterations: int, save_every: int | None = None) -> FinetuningResult:
        """Execute training loop.

        Args:
            max_iterations: Maximum number of training iterations.
            save_every: Save checkpoint every N iterations.

        Returns:
            FinetuningResult with training metrics and model path.
        """
        pass

    @abstractmethod
    def evaluate(self, prompts: list[str]) -> dict[str, Any]:
        """Evaluate model on given prompts.

        Args:
            prompts: List of prompts to evaluate.

        Returns:
            Dictionary containing prompts, responses, and rewards.
        """
        pass

    @property
    @abstractmethod
    def is_setup(self) -> bool:
        """Whether backend has been initialized."""
        pass

    @property
    def name(self) -> str:
        """Backend identifier for logging."""
        return self.__class__.__name__

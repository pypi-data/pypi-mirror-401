"""Finetuning engine facade for RLHF training."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import torch

from konic.common.errors import KonicRuntimeError, KonicValidationError
from konic.finetuning.backends import (
    BackendConfig,
    FinetuningIterationResult,
    FinetuningResult,
    NativeRLHFBackend,
)
from konic.finetuning.backends.base import BaseTrainingBackend

# Backward compatibility re-exports for tests
from konic.finetuning.backends.native import (
    ADVANTAGE_STD_THRESHOLD,  # noqa: F401
    PPOUpdater,
    compute_gae_advantages,  # noqa: F401
)
from konic.finetuning.callback import KonicFinetuningCallback
from konic.finetuning.config import (
    GenerationConfig,
    KonicFinetuningMethodType,
    TrainingConfig,
)
from konic.finetuning.dataset import DatasetLoader  # noqa: F401
from konic.finetuning.module import KonicTorchRLHF  # noqa: F401

if TYPE_CHECKING:
    from konic.finetuning.agent import BaseKonicFinetuningAgent
    from konic.finetuning.callback import BaseKonicFinetuningCallback
    from konic.finetuning.config import LoraConfig
    from konic.finetuning.dataset import DatasetConfig
    from konic.finetuning.reward import BaseKonicLLMRewardComposer

logger = logging.getLogger(__name__)


# Backend registry for method type -> backend class mapping
_BACKEND_REGISTRY: dict[KonicFinetuningMethodType, type[BaseTrainingBackend]] = {
    KonicFinetuningMethodType.NATIVE_PPO: NativeRLHFBackend,
}

# TRL backends are registered lazily (only when TRL methods are requested)
_TRL_BACKENDS_REGISTERED = False


def _register_trl_backends() -> None:
    """Register TRL backends if TRL is available."""
    global _TRL_BACKENDS_REGISTERED
    if _TRL_BACKENDS_REGISTERED:
        return

    try:
        from konic.finetuning.backends.trl import check_trl_available

        if check_trl_available():
            from konic.finetuning.backends.trl import (
                get_trl_dpo_backend,
                get_trl_grpo_backend,
            )

            _BACKEND_REGISTRY[KonicFinetuningMethodType.TRL_GRPO] = get_trl_grpo_backend()
            _BACKEND_REGISTRY[KonicFinetuningMethodType.TRL_DPO] = get_trl_dpo_backend()
            _TRL_BACKENDS_REGISTERED = True
            logger.debug("TRL backends registered successfully")
    except ImportError:
        pass  # TRL not available, skip registration


def register_backend(
    method: KonicFinetuningMethodType, backend_cls: type[BaseTrainingBackend]
) -> None:
    """Register a backend class for a finetuning method."""
    _BACKEND_REGISTRY[method] = backend_cls


class KonicFinetuningEngine:
    """Facade for LLM finetuning that delegates to pluggable backends.

    Provides a unified API for training while allowing different backends
    (native PPO, TRL GRPO, TRL DPO) to be swapped via the method parameter.
    """

    def __init__(
        self,
        model_name: str,
        reward_composer: BaseKonicLLMRewardComposer | None = None,
        dataset_config: DatasetConfig | None = None,
        lora_config: LoraConfig | None = None,
        training_config: TrainingConfig | None = None,
        generation_config: GenerationConfig | None = None,
        callback: BaseKonicFinetuningCallback | None = None,
        checkpoint_dir: str | None = None,
        device: str | None = None,
        method: KonicFinetuningMethodType = KonicFinetuningMethodType.NATIVE_PPO,
    ):
        self.model_name = model_name
        self.reward_composer = reward_composer
        self.dataset_config = dataset_config
        self.lora_config = lora_config
        self.training_config = training_config or TrainingConfig()
        self.generation_config = generation_config or GenerationConfig()
        self.callback = callback or KonicFinetuningCallback()
        self.checkpoint_dir = checkpoint_dir
        self.method = method

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self._backend: BaseTrainingBackend | None = None
        self._is_setup = False

    @classmethod
    def from_agent(cls, agent: BaseKonicFinetuningAgent) -> KonicFinetuningEngine:
        """Create engine from a finetuning agent configuration."""
        return cls(
            model_name=agent.get_base_model(),
            reward_composer=agent.get_reward_composer(),
            dataset_config=agent.get_dataset_config(),
            lora_config=agent.get_lora_config(),
            training_config=agent.get_training_config(),
            generation_config=agent.get_generation_config(),
            method=agent.get_finetuning_method(),
        )

    def _create_backend(self) -> BaseTrainingBackend:
        """Factory method to create the appropriate backend."""
        # Try to register TRL backends if a TRL method is requested
        if self.method in (
            KonicFinetuningMethodType.TRL_GRPO,
            KonicFinetuningMethodType.TRL_DPO,
        ):
            _register_trl_backends()

        if self.method not in _BACKEND_REGISTRY:
            # Provide helpful error for TRL methods
            if self.method.value.startswith("TRL_"):
                raise KonicValidationError(
                    f"TRL backend '{self.method.value}' requires the 'trl' package. "
                    "Install with: pip install konic[trl]",
                    field="method",
                )
            available = ", ".join(m.value for m in _BACKEND_REGISTRY.keys())
            raise KonicValidationError(
                f"Unknown finetuning method: {self.method.value}. Available: {available}",
                field="method",
            )

        backend_cls = _BACKEND_REGISTRY[self.method]
        return backend_cls()

    def setup(self) -> None:
        """Initialize the training backend."""
        if self._is_setup:
            return

        if self.dataset_config is None:
            raise KonicValidationError(
                "dataset_config is required for training",
                field="dataset_config",
            )

        self._backend = self._create_backend()

        backend_config = BackendConfig(
            model_name=self.model_name,
            reward_composer=self.reward_composer,
            dataset_config=self.dataset_config,
            lora_config=self.lora_config,
            training_config=self.training_config,
            generation_config=self.generation_config,
            callback=self.callback,
            checkpoint_dir=self.checkpoint_dir,
            device=self.device,
        )

        self._backend.setup(backend_config)
        self._is_setup = True

        logger.info(f"Initialized {self._backend.name} backend for {self.method.value}")

    def train(self, max_iterations: int = 100, save_every: int | None = None) -> FinetuningResult:
        """Execute training using the configured backend.

        Args:
            max_iterations: Maximum number of training iterations.
            save_every: Save checkpoint every N iterations.

        Returns:
            FinetuningResult with training metrics and model path.
        """
        self.setup()
        assert self._backend is not None
        return self._backend.train(max_iterations, save_every)

    def evaluate(self, prompts: list[str]) -> dict[str, Any]:
        """Evaluate model on given prompts.

        Args:
            prompts: List of prompts to evaluate.

        Returns:
            Dictionary containing prompts, responses, and rewards.
        """
        self.setup()
        assert self._backend is not None
        return self._backend.evaluate(prompts)

    @property
    def backend(self) -> BaseTrainingBackend | None:
        """The current training backend, None if not yet setup."""
        return self._backend

    @property
    def backend_name(self) -> str:
        """Name of the configured backend."""
        if self._backend:
            return self._backend.name
        # Return expected backend name based on method type (even before setup)
        method_to_backend = {
            KonicFinetuningMethodType.NATIVE_PPO: "NativeRLHFBackend",
            KonicFinetuningMethodType.TRL_GRPO: "TRLGRPOBackend",
            KonicFinetuningMethodType.TRL_DPO: "TRLDPOBackend",
        }
        return method_to_backend.get(self.method, "NativeRLHFBackend")

    # Backward compatibility properties - delegate to NativeRLHFBackend
    @property
    def module(self):
        """Access the underlying module (backward compatibility)."""
        if self._backend is None:
            raise KonicRuntimeError(
                "Module not initialized. Call setup() first.", operation="module_access"
            )
        if isinstance(self._backend, NativeRLHFBackend):
            return self._backend.module
        raise AttributeError("module only available for native backends")

    @property
    def dataset_loader(self):
        """Access the dataset loader (backward compatibility)."""
        if self._backend is None:
            raise KonicRuntimeError(
                "Dataset loader not initialized. Call setup() first.",
                operation="dataset_loader_access",
            )
        if isinstance(self._backend, NativeRLHFBackend):
            return self._backend.dataset_loader
        raise AttributeError("dataset_loader only available for native backends")

    @property
    def optimizer(self):
        """Access the optimizer (backward compatibility)."""
        if self._backend is None:
            raise KonicRuntimeError(
                "Optimizer not initialized. Call setup() first.", operation="optimizer_access"
            )
        if isinstance(self._backend, NativeRLHFBackend):
            return self._backend.optimizer
        raise AttributeError("optimizer only available for native backends")

    # Backward compatibility for internal methods - delegate to backend
    def _get_native_backend(self) -> NativeRLHFBackend | None:
        """Get native backend or create one for legacy test mode."""
        if isinstance(self._backend, NativeRLHFBackend):
            return self._backend
        # Legacy test mode: _module set directly or reward_composer set via constructor
        # This supports test patterns that bypass setup()
        has_module = hasattr(self, "_module") and getattr(self, "_module", None) is not None
        has_composer = self.reward_composer is not None
        if has_module or has_composer:
            return self._create_legacy_backend()
        return None

    def _create_legacy_backend(self) -> NativeRLHFBackend:
        """Create a backend wrapper for legacy test mode (internal)."""
        backend = NativeRLHFBackend()
        # Create a config for the backend (legacy mode may have None dataset_config)
        backend._config = BackendConfig(
            model_name=self.model_name,
            reward_composer=self.reward_composer,
            dataset_config=self.dataset_config,  # type: ignore[arg-type]
            lora_config=self.lora_config,
            training_config=self.training_config,
            generation_config=self.generation_config,
            callback=self.callback,
            checkpoint_dir=self.checkpoint_dir,
            device=self.device,
        )
        # Set test-provided module and optimizer if available
        backend._module = getattr(self, "_module", None)
        backend._optimizer = getattr(self, "_optimizer", None)

        # Initialize PPOUpdater if module and optimizer are available
        if backend._module is not None and backend._optimizer is not None:
            backend._ppo_updater = PPOUpdater(
                module=backend._module,
                optimizer=backend._optimizer,
                training_config=self.training_config,
                device=self.device,
            )

        backend._is_setup = True
        return backend

    def _generate_responses(self, prompts):
        """Generate responses (backward compatibility)."""
        backend = self._get_native_backend()
        if backend is None:
            raise AttributeError("_generate_responses only available for native backends")
        return backend._generate_responses(prompts)

    def _compute_rewards(self, prompts, responses):
        """Compute rewards (backward compatibility)."""
        backend = self._get_native_backend()
        if backend is None:
            raise AttributeError("_compute_rewards only available for native backends")
        return backend._compute_rewards(prompts, responses)

    def _ppo_update(self, input_ids, response_ids, rewards):
        """PPO update (backward compatibility)."""
        backend = self._get_native_backend()
        if backend is None:
            raise AttributeError("_ppo_update only available for native backends")
        return backend._ppo_update(input_ids, response_ids, rewards)

    def _compute_advantages(self, rewards, values, gamma, gae_lambda):
        """Compute GAE advantages (backward compatibility)."""
        backend = self._get_native_backend()
        if backend is None:
            raise AttributeError("_compute_advantages only available for native backends")
        return backend._compute_advantages(rewards, values, gamma, gae_lambda)

    def _save_checkpoint(self, iteration):
        """Save checkpoint (backward compatibility)."""
        backend = self._get_native_backend()
        if backend is None:
            raise AttributeError("_save_checkpoint only available for native backends")
        return backend._save_checkpoint(iteration)

    def train_iter(self, iteration):
        """Run single training iteration (backward compatibility)."""
        backend = self._get_native_backend()
        if backend is None:
            raise AttributeError("train_iter only available for native backends")
        return backend._train_iteration(iteration)


__all__ = [
    "FinetuningIterationResult",
    "FinetuningResult",
    "KonicFinetuningEngine",
    # Backward compatibility re-exports
    "ADVANTAGE_STD_THRESHOLD",
    "DatasetLoader",
    "KonicTorchRLHF",
]

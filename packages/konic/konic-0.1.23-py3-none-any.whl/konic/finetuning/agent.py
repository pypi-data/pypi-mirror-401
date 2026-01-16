"""Agent classes for LLM finetuning."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from konic.agent.base import BaseKonicAgent
from konic.common.errors import KonicConfigurationError, KonicValidationError
from konic.finetuning.config import (
    GenerationConfig,
    KonicFinetuningMethodType,
    LoraConfig,
    TrainingConfig,
)

if TYPE_CHECKING:
    from konic.finetuning.dataset import DatasetConfig
    from konic.finetuning.environment import BaseKonicLLMEnvironment
    from konic.finetuning.module import BaseKonicLLMModule
    from konic.finetuning.reward import BaseKonicLLMRewardComposer


class BaseKonicFinetuningAgent(BaseKonicAgent, ABC):
    """Abstract base class for LLM finetuning agents."""

    @abstractmethod
    def get_base_model(self) -> str:
        pass

    @abstractmethod
    def get_finetuning_method(self) -> KonicFinetuningMethodType:
        pass

    @abstractmethod
    def get_lora_config(self) -> LoraConfig | None:
        pass

    @abstractmethod
    def get_reward_composer(self) -> "BaseKonicLLMRewardComposer":
        pass

    @abstractmethod
    def get_dataset_config(self) -> "DatasetConfig":
        pass

    @abstractmethod
    def get_environment(self) -> "BaseKonicLLMEnvironment":
        pass

    @abstractmethod
    def get_module(self) -> "type[BaseKonicLLMModule] | None":  # type: ignore[override]
        pass

    @abstractmethod
    def get_training_config(self) -> TrainingConfig:  # type: ignore[override]
        pass

    @abstractmethod
    def get_generation_config(self) -> GenerationConfig:
        pass


class KonicFinetuningAgent(BaseKonicFinetuningAgent):
    """Concrete finetuning agent with constructor-based configuration."""

    def __init__(
        self,
        base_model: str,
        environment: "BaseKonicLLMEnvironment | None" = None,
        reward_composer: "BaseKonicLLMRewardComposer | None" = None,
        module: "type[BaseKonicLLMModule] | None" = None,
        lora_config: LoraConfig | None = None,
        dataset_config: "DatasetConfig | None" = None,
        training_config: TrainingConfig | dict[str, Any] | None = None,
        generation_config: GenerationConfig | dict[str, Any] | None = None,
        method: KonicFinetuningMethodType = KonicFinetuningMethodType.NATIVE_PPO,
    ):
        self._base_model = base_model
        self._method = method
        self._environment = environment
        self._reward_composer = reward_composer
        self._lora_config = lora_config
        self._dataset_config = dataset_config

        # Handle training config
        if training_config is None:
            self._training_config = TrainingConfig()
        elif isinstance(training_config, dict):
            self._training_config = TrainingConfig(**training_config)
        else:
            self._training_config = training_config

        # Handle generation config
        if generation_config is None:
            self._generation_config = GenerationConfig()
        elif isinstance(generation_config, dict):
            self._generation_config = GenerationConfig(**generation_config)
        else:
            self._generation_config = generation_config

        # Set default module based on method
        if module is None:
            self._module = self._get_default_module()
        else:
            self._module = module

        # Track what was explicitly provided
        self._has_environment = environment is not None
        self._has_reward_composer = reward_composer is not None
        self._has_dataset_config = dataset_config is not None

    def _get_default_module(self) -> "type[BaseKonicLLMModule]":
        from konic.finetuning.module import KonicTorchRLHF

        native_methods = {
            KonicFinetuningMethodType.NATIVE_PPO,
        }
        trl_methods = {
            KonicFinetuningMethodType.TRL_GRPO,
            KonicFinetuningMethodType.TRL_DPO,
        }

        if self._method in native_methods:
            return KonicTorchRLHF
        elif self._method in trl_methods:
            # TRL backends handle model loading internally
            return KonicTorchRLHF  # Placeholder, TRL backends don't use this
        else:
            raise KonicValidationError(
                f"Unknown finetuning method: {self._method}",
                field="method",
            )

    def get_base_model(self) -> str:
        return self._base_model

    def get_finetuning_method(self) -> KonicFinetuningMethodType:
        return self._method

    def get_lora_config(self) -> LoraConfig | None:
        return self._lora_config

    def get_reward_composer(self) -> "BaseKonicLLMRewardComposer":
        if self._reward_composer is None:
            raise KonicConfigurationError(
                "Reward composer is required for RLHF training. "
                "Please provide a reward_composer in the constructor.",
                config_key="reward_composer",
            )
        return self._reward_composer

    def get_dataset_config(self) -> "DatasetConfig":
        if self._dataset_config is None:
            raise KonicConfigurationError(
                "Dataset configuration is required for training. "
                "Please provide a dataset_config in the constructor.",
                config_key="dataset_config",
            )
        return self._dataset_config

    def get_environment(self) -> "BaseKonicLLMEnvironment":
        if self._environment is None:
            raise KonicConfigurationError(
                "Environment is required for training. "
                "Please provide an environment in the constructor.",
                config_key="environment",
            )
        return self._environment

    def get_environment_config(self) -> dict[str, Any]:
        return self._generation_config.to_dict()

    def get_algorithm_config(self) -> dict[str, Any]:
        return {
            "learning_rate": self._training_config.learning_rate,
            "clip_ratio": self._training_config.clip_ratio,
            "entropy_coef": self._training_config.entropy_coef,
            "vf_coef": self._training_config.vf_coef,
            "max_grad_norm": self._training_config.max_grad_norm,
            "gamma": self._training_config.gamma,
            "gae_lambda": self._training_config.gae_lambda,
        }

    def get_module(self) -> "type[BaseKonicLLMModule]":
        return self._module

    def get_training_config(self) -> TrainingConfig:
        return self._training_config

    def get_generation_config(self) -> GenerationConfig:
        return self._generation_config

    @property
    def training_config(self) -> TrainingConfig:
        return self._training_config

    @property
    def generation_config(self) -> GenerationConfig:
        return self._generation_config

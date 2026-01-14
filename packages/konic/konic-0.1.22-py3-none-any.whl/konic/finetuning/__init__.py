"""Konic LLM Finetuning Module.

This module provides RL-based finetuning capabilities for Large Language Models.
Supports multiple training backends:
- Native PPO (default): Custom RLHF implementation with PPO algorithm
- TRL GRPO: Group Relative Policy Optimization via HuggingFace TRL
- TRL DPO: Direct Preference Optimization via HuggingFace TRL

Example (Native PPO):
    >>> from konic.finetuning import (
    ...     KonicFinetuningAgent,
    ...     KonicLLMRewardComposer,
    ...     KonicFinetuningEngine,
    ...     LoraConfig,
    ...     llm_reward,
    ... )
    >>> from konic.finetuning.dataset import DatasetConfig
    >>>
    >>> class MyRewardComposer(KonicLLMRewardComposer):
    ...     @llm_reward
    ...     def brevity_bonus(self, prompt: str, response: str) -> float:
    ...         return max(0, 1.0 - len(response) / 500)
    >>>
    >>> agent = KonicFinetuningAgent(
    ...     base_model="Qwen/Qwen2-0.5B-Instruct",
    ...     reward_composer=MyRewardComposer(),
    ...     lora_config=LoraConfig(r=16),
    ...     dataset_config=DatasetConfig(name="imdb"),
    ... )
    >>>
    >>> engine = KonicFinetuningEngine.from_agent(agent)
    >>> result = engine.train(max_iterations=100)

Example (TRL GRPO):
    >>> from konic.finetuning import (
    ...     KonicFinetuningAgent,
    ...     KonicFinetuningMethodType,
    ... )
    >>>
    >>> agent = KonicFinetuningAgent(
    ...     base_model="Qwen/Qwen2-0.5B-Instruct",
    ...     reward_composer=MyRewardComposer(),
    ...     method=KonicFinetuningMethodType.TRL_GRPO,
    ... )
"""

# Config
# Agent
from konic.finetuning.agent import (
    BaseKonicFinetuningAgent,
    KonicFinetuningAgent,
)

# Backends
from konic.finetuning.backends import (
    BackendConfig,
    BaseTrainingBackend,
    NativeRLHFBackend,
)

# Callback
from konic.finetuning.callback import (
    BaseKonicFinetuningCallback,
    CompositeCallback,
    KonicFinetuningCallback,
)
from konic.finetuning.config import (
    GenerationConfig,
    KonicFinetuningMethodType,
    LoraConfig,
    TrainingConfig,
)

# Dataset
from konic.finetuning.dataset import (
    DatasetConfig,
    DatasetLoader,
    DatasetSource,
    PreferenceDatasetConfig,
    PromptDatasetConfig,
)

# Engine
from konic.finetuning.engine import (
    FinetuningIterationResult,
    FinetuningResult,
    KonicFinetuningEngine,
)

# Environment
from konic.finetuning.environment import (
    BaseKonicLLMEnvironment,
    KonicLLMEnvironment,
    PromptTemplate,
    TokenizerWrapper,
)

# Module
from konic.finetuning.module import (
    BaseKonicLLMModule,
    ForwardAllOutput,
    KonicTorchRLHF,
    ValueHead,
    apply_lora,
    count_trainable_parameters,
    get_lora_state_dict,
    get_target_modules_for_model,
)

# Reward
from konic.finetuning.reward import (
    BaseKonicLLMRewardComposer,
    BaseRewardModel,
    BaseRewardReducer,
    HuggingFaceRewardModel,
    KonicLLMRewardComposer,
    MaxReducer,
    MeanReducer,
    WeightedSumReducer,
    llm_reward,
)

__all__ = [
    # Config
    "LoraConfig",
    "TrainingConfig",
    "GenerationConfig",
    "KonicFinetuningMethodType",
    # Module
    "BaseKonicLLMModule",
    "ForwardAllOutput",
    "KonicTorchRLHF",
    "ValueHead",
    "apply_lora",
    "get_lora_state_dict",
    "count_trainable_parameters",
    "get_target_modules_for_model",
    # Agent
    "BaseKonicFinetuningAgent",
    "KonicFinetuningAgent",
    # Environment
    "BaseKonicLLMEnvironment",
    "KonicLLMEnvironment",
    "TokenizerWrapper",
    "PromptTemplate",
    # Reward
    "BaseKonicLLMRewardComposer",
    "KonicLLMRewardComposer",
    "llm_reward",
    "BaseRewardModel",
    "HuggingFaceRewardModel",
    "BaseRewardReducer",
    "WeightedSumReducer",
    "MeanReducer",
    "MaxReducer",
    # Dataset
    "DatasetConfig",
    "DatasetSource",
    "DatasetLoader",
    "PromptDatasetConfig",
    "PreferenceDatasetConfig",
    # Engine
    "KonicFinetuningEngine",
    "FinetuningResult",
    "FinetuningIterationResult",
    # Backends
    "BackendConfig",
    "BaseTrainingBackend",
    "NativeRLHFBackend",
    # Callback
    "BaseKonicFinetuningCallback",
    "KonicFinetuningCallback",
    "CompositeCallback",
]

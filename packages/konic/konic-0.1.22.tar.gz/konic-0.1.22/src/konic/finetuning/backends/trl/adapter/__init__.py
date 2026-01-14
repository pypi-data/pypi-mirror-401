"""TRL adapter implementations bridging Konic to TRL interfaces."""

from konic.finetuning.backends.trl.adapter.callback import create_trl_callback_adapter
from konic.finetuning.backends.trl.adapter.config import (
    generation_config_to_kwargs,
    lora_config_to_peft_config,
    training_config_to_dpo_config,
    training_config_to_grpo_config,
)
from konic.finetuning.backends.trl.adapter.reward import (
    adapt_hf_reward_model,
    adapt_reward_composer_to_trl,
    create_reward_func_from_callable,
)

__all__ = [
    # Callback adapter
    "create_trl_callback_adapter",
    # Config mappers
    "generation_config_to_kwargs",
    "lora_config_to_peft_config",
    "training_config_to_dpo_config",
    "training_config_to_grpo_config",
    # Reward adapters
    "adapt_hf_reward_model",
    "adapt_reward_composer_to_trl",
    "create_reward_func_from_callable",
]

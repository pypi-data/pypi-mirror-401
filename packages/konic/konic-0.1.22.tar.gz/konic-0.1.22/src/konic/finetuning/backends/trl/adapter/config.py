"""Map Konic configuration classes to TRL configuration classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from konic.finetuning.backends.trl.base import require_trl

if TYPE_CHECKING:
    from konic.finetuning.config import GenerationConfig, LoraConfig, TrainingConfig


def training_config_to_grpo_config(
    training_config: TrainingConfig,
    generation_config: GenerationConfig | None = None,
    output_dir: str = "./grpo_output",
    max_steps: int = 100,
    **kwargs: Any,
):
    """Convert Konic TrainingConfig to TRL GRPOConfig."""
    require_trl()
    from trl import GRPOConfig  # type: ignore[attr-defined]

    # GRPO requires batch_size to be divisible by num_generations
    batch_size = training_config.batch_size
    num_generations = kwargs.get("num_generations", 4)

    # Ensure constraint: batch_size must be divisible by num_generations
    if batch_size < num_generations:
        num_generations = batch_size
    elif batch_size % num_generations != 0:
        # Find largest divisor of batch_size that's <= original num_generations
        for n in range(num_generations, 0, -1):
            if batch_size % n == 0:
                num_generations = n
                break

    # Build config with training parameters
    config_kwargs: dict[str, Any] = {
        "output_dir": output_dir,
        "max_steps": max_steps,
        "learning_rate": training_config.learning_rate,
        "per_device_train_batch_size": batch_size,
        "gradient_accumulation_steps": training_config.gradient_accumulation_steps,
        "max_grad_norm": training_config.max_grad_norm,
        "beta": training_config.kl_penalty_weight,
        "report_to": [],  # Disable default reporters
        "logging_steps": kwargs.get("logging_steps", 1),
        "save_steps": kwargs.get("save_steps", 100),
        "num_generations": num_generations,
        # Note: We handle prompt truncation in grpo.py before passing to trainer
    }

    # Add generation parameters if provided (TRL uses different param names)
    if generation_config is not None:
        config_kwargs["max_completion_length"] = generation_config.max_new_tokens
        config_kwargs["temperature"] = generation_config.temperature
        if generation_config.top_k > 0:
            config_kwargs["top_k"] = generation_config.top_k

    # Filter valid extra kwargs (exclude generation params that were handled above)
    excluded_keys = {
        "use_mlflow",
        "logging_steps",
        "save_steps",
        "num_generations",
        "max_new_tokens",
        "min_new_tokens",
        "top_p",
        "do_sample",
        "repetition_penalty",
        "pad_token_id",
        "eos_token_id",
    }
    for k, v in kwargs.items():
        if k not in excluded_keys:
            config_kwargs[k] = v

    return GRPOConfig(**config_kwargs)


def training_config_to_dpo_config(
    training_config: TrainingConfig,
    output_dir: str = "./dpo_output",
    max_steps: int = 100,
    **kwargs: Any,
):
    """Convert Konic TrainingConfig to TRL DPOConfig."""
    require_trl()
    from trl import DPOConfig  # type: ignore[attr-defined]

    return DPOConfig(
        output_dir=output_dir,
        max_steps=max_steps,
        learning_rate=training_config.learning_rate,
        per_device_train_batch_size=training_config.batch_size,
        gradient_accumulation_steps=training_config.gradient_accumulation_steps,
        max_grad_norm=training_config.max_grad_norm,
        beta=training_config.kl_penalty_weight,
        report_to=["mlflow"] if kwargs.get("use_mlflow", True) else [],
        logging_steps=kwargs.get("logging_steps", 1),
        save_steps=kwargs.get("save_steps", 100),
        **{
            k: v
            for k, v in kwargs.items()
            if k not in ("use_mlflow", "logging_steps", "save_steps")
        },
    )


def lora_config_to_peft_config(lora_config: LoraConfig | None):
    """Convert Konic LoraConfig to PEFT LoraConfig."""
    if lora_config is None:
        return None
    return lora_config.to_peft_config()


def generation_config_to_kwargs(gen_config: GenerationConfig) -> dict[str, Any]:
    """Convert Konic GenerationConfig to generation kwargs dict."""
    kwargs = {
        "max_new_tokens": gen_config.max_new_tokens,
        "min_new_tokens": gen_config.min_new_tokens,
        "temperature": gen_config.temperature,
        "top_p": gen_config.top_p,
        "do_sample": gen_config.do_sample,
        "repetition_penalty": gen_config.repetition_penalty,
    }

    if gen_config.top_k > 0:
        kwargs["top_k"] = gen_config.top_k

    if gen_config.pad_token_id is not None:
        kwargs["pad_token_id"] = gen_config.pad_token_id

    if gen_config.eos_token_id is not None:
        kwargs["eos_token_id"] = gen_config.eos_token_id

    return kwargs

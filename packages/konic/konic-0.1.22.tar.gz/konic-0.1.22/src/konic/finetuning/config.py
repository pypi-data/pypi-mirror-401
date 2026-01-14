"""Configuration classes for LLM finetuning."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal

from konic.common.errors import KonicValidationError


class KonicFinetuningMethodType(str, Enum):
    """Available LLM finetuning methods.

    Migration Note:
        The deprecated 'RLHF' method type has been removed. Use 'NATIVE_PPO' instead.
        Both refer to the same native PPO-based RLHF implementation. Existing code
        using method="RLHF" should be updated to method="NATIVE_PPO" or simply
        omit the method parameter (NATIVE_PPO is now the default).
    """

    # Native backend (Konic's PPO implementation)
    NATIVE_PPO = "NATIVE_PPO"

    # TRL backend methods (requires trl package)
    TRL_GRPO = "TRL_GRPO"  # Group Relative Policy Optimization
    TRL_DPO = "TRL_DPO"  # Direct Preference Optimization


@dataclass
class LoraConfig:
    """LoRA adapter configuration for parameter-efficient finetuning."""

    r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: list[str] = field(default_factory=lambda: ["q_proj", "v_proj"])
    bias: Literal["none", "all", "lora_only"] = "none"
    task_type: str = "CAUSAL_LM"
    fan_in_fan_out: bool = False

    def to_peft_config(self):
        from peft import LoraConfig as PeftLoraConfig

        return PeftLoraConfig(
            r=self.r,
            lora_alpha=self.lora_alpha,
            lora_dropout=self.lora_dropout,
            target_modules=self.target_modules,
            bias=self.bias,
            task_type=self.task_type,
            fan_in_fan_out=self.fan_in_fan_out,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "r": self.r,
            "lora_alpha": self.lora_alpha,
            "lora_dropout": self.lora_dropout,
            "target_modules": self.target_modules,
            "bias": self.bias,
            "task_type": self.task_type,
        }


@dataclass
class TrainingConfig:
    """RLHF/PPO training hyperparameters."""

    learning_rate: float = 1e-5
    samples_per_iteration: int = 1
    batch_size: int = 8
    gradient_accumulation_steps: int = 4
    max_grad_norm: float = 1.0
    kl_penalty_weight: float = 0.1
    clip_ratio: float = 0.2
    vf_coef: float = 0.5
    entropy_coef: float = 0.01
    gamma: float = 1.0
    gae_lambda: float = 0.95
    ppo_epochs: int = 4
    warmup_steps: int = 100
    weight_decay: float = 0.01

    def __post_init__(self) -> None:
        if self.learning_rate <= 0:
            raise KonicValidationError(
                f"learning_rate must be positive, got {self.learning_rate}",
                field="learning_rate",
            )
        if not 0 <= self.gamma <= 1:
            raise KonicValidationError(
                f"gamma must be in range [0, 1], got {self.gamma}",
                field="gamma",
            )
        if not 0 <= self.gae_lambda <= 1:
            raise KonicValidationError(
                f"gae_lambda must be in range [0, 1], got {self.gae_lambda}",
                field="gae_lambda",
            )
        if self.clip_ratio <= 0:
            raise KonicValidationError(
                f"clip_ratio must be positive, got {self.clip_ratio}",
                field="clip_ratio",
            )

    @property
    def effective_batch_size(self) -> int:
        return self.batch_size * self.gradient_accumulation_steps

    def to_dict(self) -> dict[str, Any]:
        return {
            "learning_rate": self.learning_rate,
            "samples_per_iteration": self.samples_per_iteration,
            "batch_size": self.batch_size,
            "gradient_accumulation_steps": self.gradient_accumulation_steps,
            "max_grad_norm": self.max_grad_norm,
            "kl_penalty_weight": self.kl_penalty_weight,
            "clip_ratio": self.clip_ratio,
            "vf_coef": self.vf_coef,
            "entropy_coef": self.entropy_coef,
            "gamma": self.gamma,
            "gae_lambda": self.gae_lambda,
            "ppo_epochs": self.ppo_epochs,
            "warmup_steps": self.warmup_steps,
            "weight_decay": self.weight_decay,
        }

    @classmethod
    def fast_debug(cls) -> "TrainingConfig":
        """Minimal config for debugging. Not for production."""
        return cls(
            learning_rate=1e-4,
            batch_size=2,
            gradient_accumulation_steps=1,
            ppo_epochs=1,
            warmup_steps=0,
            kl_penalty_weight=0.0,
        )

    @classmethod
    def cpu_optimized(cls) -> "TrainingConfig":
        """Config with smaller batches for CPU training."""
        return cls(
            learning_rate=5e-5,
            batch_size=1,
            gradient_accumulation_steps=8,
            ppo_epochs=2,
            max_grad_norm=0.5,
        )

    @classmethod
    def gpu_optimized(cls) -> "TrainingConfig":
        """Config with larger batches for GPU training."""
        return cls(
            learning_rate=1e-5,
            batch_size=16,
            gradient_accumulation_steps=2,
            ppo_epochs=4,
            kl_penalty_weight=0.1,
            entropy_coef=0.01,
        )


@dataclass
class GenerationConfig:
    """Text generation settings for RLHF rollouts."""

    max_new_tokens: int = 128
    min_new_tokens: int = 1
    max_length: int = 512
    max_prompt_length: int = 256
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = 0
    do_sample: bool = True
    repetition_penalty: float = 1.0
    pad_token_id: int | None = None
    eos_token_id: int | list[int] | None = None

    def to_dict(self) -> dict[str, Any]:
        config = {
            "max_new_tokens": self.max_new_tokens,
            "min_new_tokens": self.min_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "do_sample": self.do_sample,
            "repetition_penalty": self.repetition_penalty,
        }

        if self.top_k > 0:
            config["top_k"] = self.top_k

        if self.pad_token_id is not None:
            config["pad_token_id"] = self.pad_token_id

        if self.eos_token_id is not None:
            config["eos_token_id"] = self.eos_token_id

        return config

"""Result dataclasses for finetuning training."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FinetuningIterationResult:
    """Metrics from a single training iteration."""

    iteration: int
    reward_mean: float
    reward_std: float = 0.0
    reward_min: float = 0.0
    reward_max: float = 0.0
    kl_divergence: float = 0.0
    policy_loss: float = 0.0
    value_loss: float = 0.0
    entropy_loss: float = 0.0
    total_loss: float = 0.0
    response_length_mean: float = 0.0
    response_length_std: float = 0.0
    learning_rate: float = 0.0
    clip_fraction: float = 0.0
    approx_kl: float = 0.0
    explained_variance: float = 0.0

    reward_breakdown: dict[str, float] = field(default_factory=dict)
    generation_time_sec: float = 0.0
    reward_compute_time_sec: float = 0.0
    update_time_sec: float = 0.0
    total_time_sec: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "iteration": self.iteration,
            "reward/mean": self.reward_mean,
            "reward/std": self.reward_std,
            "reward/min": self.reward_min,
            "reward/max": self.reward_max,
            "kl/divergence": self.kl_divergence,
            "loss/policy": self.policy_loss,
            "loss/value": self.value_loss,
            "loss/entropy": self.entropy_loss,
            "loss/total": self.total_loss,
            "response/length_mean": self.response_length_mean,
            "response/length_std": self.response_length_std,
            "train/learning_rate": self.learning_rate,
            "train/clip_fraction": self.clip_fraction,
            "train/approx_kl": self.approx_kl,
            "train/explained_variance": self.explained_variance,
            "time/generation_sec": self.generation_time_sec,
            "time/reward_sec": self.reward_compute_time_sec,
            "time/update_sec": self.update_time_sec,
            "time/total_sec": self.total_time_sec,
            **{f"reward/{k}": v for k, v in self.reward_breakdown.items()},
        }


@dataclass
class FinetuningResult:
    """Aggregated results from a finetuning run.

    Reward Semantics by Backend:
        - NATIVE_PPO / TRL_GRPO: Rewards are computed from reward composer functions.
          Higher values indicate better alignment with reward objectives.
        - TRL_DPO: Rewards are derived as -loss (negated loss). Since lower DPO loss
          indicates better preference alignment, negating produces higher rewards for
          better models. Note that DPO rewards will typically be negative values.
    """

    total_iterations: int
    best_iteration: int = 0
    best_reward: float = float("-inf")
    final_reward_mean: float = 0.0
    final_kl_divergence: float = 0.0
    total_samples: int = 0
    total_time_sec: float = 0.0
    model_path: str | None = None
    history: list[FinetuningIterationResult] = field(default_factory=list)

    model_name: str = ""
    lora_config: dict | None = None
    training_config: dict | None = None

    def add_iteration_result(self, result: FinetuningIterationResult) -> None:
        self.history.append(result)
        self.total_iterations = result.iteration
        if result.reward_mean > self.best_reward:
            self.best_reward = result.reward_mean
            self.best_iteration = result.iteration
        self.final_reward_mean = result.reward_mean
        self.final_kl_divergence = result.kl_divergence
        self.total_time_sec += result.total_time_sec

    def get_reward_curve(self) -> list[float]:
        return [r.reward_mean for r in self.history]

    def get_kl_curve(self) -> list[float]:
        return [r.kl_divergence for r in self.history]

    def get_loss_curves(self) -> dict[str, list[float]]:
        return {
            "policy": [r.policy_loss for r in self.history],
            "value": [r.value_loss for r in self.history],
            "entropy": [r.entropy_loss for r in self.history],
            "total": [r.total_loss for r in self.history],
        }

    def summary(self) -> str:
        lines = [
            "=" * 50,
            "Finetuning Results Summary",
            "=" * 50,
            f"Model: {self.model_name}",
            f"Total Iterations: {self.total_iterations}",
            f"Total Samples: {self.total_samples}",
            f"Total Time: {self.total_time_sec:.1f}s",
            "-" * 50,
            f"Best Reward: {self.best_reward:.4f} (iteration {self.best_iteration})",
            f"Final Reward: {self.final_reward_mean:.4f}",
            f"Final KL Divergence: {self.final_kl_divergence:.4f}",
            "-" * 50,
        ]

        if self.model_path:
            lines.append(f"Model saved to: {self.model_path}")

        lines.append("=" * 50)
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_iterations": self.total_iterations,
            "best_iteration": self.best_iteration,
            "best_reward": self.best_reward,
            "final_reward_mean": self.final_reward_mean,
            "final_kl_divergence": self.final_kl_divergence,
            "total_samples": self.total_samples,
            "total_time_sec": self.total_time_sec,
            "model_path": self.model_path,
            "model_name": self.model_name,
            "lora_config": self.lora_config,
            "training_config": self.training_config,
            "history": [r.to_dict() for r in self.history],
        }

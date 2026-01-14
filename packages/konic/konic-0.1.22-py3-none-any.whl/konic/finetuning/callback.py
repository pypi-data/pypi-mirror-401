"""Callbacks for RLHF training monitoring and control."""

from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING, Any

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from konic.finetuning.engine import FinetuningIterationResult, FinetuningResult


class BaseKonicFinetuningCallback(ABC):
    """Abstract base class for finetuning callbacks."""

    def on_train_begin(self, config: dict[str, Any]) -> None:
        pass

    def on_train_end(self, result: FinetuningResult) -> None:
        pass

    def on_iteration_begin(self, iteration: int) -> None:
        pass

    def on_iteration_end(self, result: FinetuningIterationResult) -> None:
        pass

    def on_generation_begin(self, prompts: list[str]) -> None:
        pass

    def on_generation_end(
        self,
        prompts: list[str],
        responses: list[str],
    ) -> None:
        pass

    def on_reward_computed(
        self,
        rewards: list[float],
        reward_breakdown: dict[str, list[float]],
    ) -> None:
        pass

    def on_checkpoint_saved(self, path: str, iteration: int) -> None:
        pass

    def should_stop_early(self, result: FinetuningIterationResult) -> bool:
        return False


class KonicFinetuningCallback(BaseKonicFinetuningCallback):
    """Default callback with logging, MLflow integration, and early stopping."""

    def __init__(
        self,
        log_interval: int = 1,
        log_samples: bool = False,
        max_samples_to_log: int = 3,
        use_mlflow: bool = True,
        early_stop_kl_threshold: float | None = None,
        early_stop_patience: int = 5,
        verbose: bool = True,
    ):
        self.log_interval = log_interval
        self.log_samples = log_samples
        self.max_samples_to_log = max_samples_to_log
        self.use_mlflow = use_mlflow
        self.early_stop_kl_threshold = early_stop_kl_threshold
        self.early_stop_patience = early_stop_patience
        self.verbose = verbose

        # Track early stopping state
        self._high_kl_count = 0
        self._mlflow_initialized = False

        # Store samples for logging
        self._current_prompts: list[str] = []
        self._current_responses: list[str] = []

    def on_train_begin(self, config: dict[str, Any]) -> None:
        if self.verbose:
            print("\n" + "=" * 60)
            print("Starting RLHF Training")
            print("=" * 60)
            print(f"Model: {config.get('model_name', 'unknown')}")
            print(f"LoRA: {config.get('use_lora', False)}")
            print(f"Learning Rate: {config.get('learning_rate', 'N/A')}")
            print(f"Batch Size: {config.get('batch_size', 'N/A')}")
            print(f"Max Iterations: {config.get('max_iterations', 'N/A')}")
            print("=" * 60 + "\n")

        if self.use_mlflow:
            self._init_mlflow(config)

    def on_train_end(self, result: FinetuningResult) -> None:
        if self.verbose:
            print("\n" + result.summary())

        if self.use_mlflow and self._mlflow_initialized:
            import mlflow  # type: ignore[import-not-found]

            mlflow.log_metric("final/reward_mean", result.final_reward_mean)
            mlflow.log_metric("final/best_reward", result.best_reward)
            mlflow.log_metric("final/best_iteration", result.best_iteration)
            mlflow.log_metric("final/total_time_sec", result.total_time_sec)

    def on_iteration_end(self, result: FinetuningIterationResult) -> None:
        if result.iteration % self.log_interval == 0:
            if self.verbose:
                self._log_iteration_console(result)

            if self.use_mlflow and self._mlflow_initialized:
                self._log_iteration_mlflow(result)

        # Log samples if enabled
        if self.log_samples and self._current_prompts:
            self._log_samples(result.iteration)

    def on_generation_end(
        self,
        prompts: list[str],
        responses: list[str],
    ) -> None:
        self._current_prompts = prompts[: self.max_samples_to_log]
        self._current_responses = responses[: self.max_samples_to_log]

    def should_stop_early(self, result: FinetuningIterationResult) -> bool:
        if self.early_stop_kl_threshold is None:
            return False

        if result.kl_divergence > self.early_stop_kl_threshold:
            self._high_kl_count += 1
            if self.verbose:
                print(
                    f"Warning: KL divergence ({result.kl_divergence:.4f}) exceeds "
                    f"threshold ({self.early_stop_kl_threshold}). "
                    f"Count: {self._high_kl_count}/{self.early_stop_patience}"
                )

            if self._high_kl_count >= self.early_stop_patience:
                if self.verbose:
                    print("Early stopping triggered due to high KL divergence.")
                return True
        else:
            self._high_kl_count = 0

        return False

    def on_checkpoint_saved(self, path: str, iteration: int) -> None:
        if self.verbose:
            print(f"Checkpoint saved: {path} (iteration {iteration})")

        if self.use_mlflow and self._mlflow_initialized:
            import mlflow  # type: ignore[import-not-found]

            mlflow.log_artifact(path)

    def _log_iteration_console(self, result: FinetuningIterationResult) -> None:
        print(
            f"[Iter {result.iteration:4d}] "
            f"Reward: {result.reward_mean:7.3f} (+/- {result.reward_std:.3f}) | "
            f"KL: {result.kl_divergence:.4f} | "
            f"Loss: {result.total_loss:.4f} | "
            f"Time: {result.total_time_sec:.1f}s"
        )

    def _log_iteration_mlflow(self, result: FinetuningIterationResult) -> None:
        import mlflow  # type: ignore[import-not-found]

        metrics = result.to_dict()
        step = result.iteration

        for key, value in metrics.items():
            if isinstance(value, (int | float)) and key != "iteration":
                mlflow.log_metric(key, value, step=step)

    def _log_samples(self, iteration: int) -> None:
        if self.verbose:
            print(f"\n--- Sample Generations (Iteration {iteration}) ---")
            for i, (prompt, response) in enumerate(
                zip(self._current_prompts, self._current_responses)
            ):
                print(f"\n[Sample {i + 1}]")
                print(f"Prompt: {prompt[:200]}...")
                print(f"Response: {response[:500]}...")
            print("-" * 50 + "\n")

        # Clear stored samples
        self._current_prompts = []
        self._current_responses = []

    def _init_mlflow(self, config: dict[str, Any]) -> None:
        try:
            import mlflow  # type: ignore[import-not-found]

            # Log config as params
            for key, value in config.items():
                if isinstance(value, (str | int | float | bool)):
                    mlflow.log_param(key, value)

            self._mlflow_initialized = True
        except ImportError:
            logger.warning("MLflow not installed. Skipping MLflow logging.")
            self.use_mlflow = False
        except Exception as e:
            logger.warning(f"Failed to initialize MLflow: {e}")
            self.use_mlflow = False


class CompositeCallback(BaseKonicFinetuningCallback):
    """Combines multiple callbacks into one."""

    def __init__(self, callbacks: list[BaseKonicFinetuningCallback]):
        self.callbacks = callbacks

    def on_train_begin(self, config: dict[str, Any]) -> None:
        for cb in self.callbacks:
            cb.on_train_begin(config)

    def on_train_end(self, result: FinetuningResult) -> None:
        for cb in self.callbacks:
            cb.on_train_end(result)

    def on_iteration_begin(self, iteration: int) -> None:
        for cb in self.callbacks:
            cb.on_iteration_begin(iteration)

    def on_iteration_end(self, result: FinetuningIterationResult) -> None:
        for cb in self.callbacks:
            cb.on_iteration_end(result)

    def on_generation_begin(self, prompts: list[str]) -> None:
        for cb in self.callbacks:
            cb.on_generation_begin(prompts)

    def on_generation_end(
        self,
        prompts: list[str],
        responses: list[str],
    ) -> None:
        for cb in self.callbacks:
            cb.on_generation_end(prompts, responses)

    def on_reward_computed(
        self,
        rewards: list[float],
        reward_breakdown: dict[str, list[float]],
    ) -> None:
        for cb in self.callbacks:
            cb.on_reward_computed(rewards, reward_breakdown)

    def on_checkpoint_saved(self, path: str, iteration: int) -> None:
        for cb in self.callbacks:
            cb.on_checkpoint_saved(path, iteration)

    def should_stop_early(self, result: FinetuningIterationResult) -> bool:
        # Stop if any callback requests it
        return any(cb.should_stop_early(result) for cb in self.callbacks)

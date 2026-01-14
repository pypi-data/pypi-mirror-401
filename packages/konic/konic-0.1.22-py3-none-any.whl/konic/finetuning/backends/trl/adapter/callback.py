"""Adapt Konic finetuning callbacks to TRL TrainerCallback interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from konic.finetuning.backends.result import FinetuningIterationResult
from konic.finetuning.backends.trl.base import require_trl

if TYPE_CHECKING:
    from konic.finetuning.callback import BaseKonicFinetuningCallback


def create_trl_callback_adapter(
    konic_callback: BaseKonicFinetuningCallback,
):
    """Create a TRL TrainerCallback that delegates to Konic callback.

    This adapter bridges TRL's callback system with Konic's callback system,
    ensuring that Konic callbacks work seamlessly with TRL trainers.
    """
    require_trl()
    from transformers import TrainerCallback, TrainerControl, TrainerState, TrainingArguments

    class TRLCallbackAdapter(TrainerCallback):
        """Adapts Konic callbacks to TRL TrainerCallback interface."""

        def __init__(self, konic_cb: BaseKonicFinetuningCallback):
            self._konic = konic_cb
            self._step_metrics: dict[str, Any] = {}

        def on_train_begin(
            self,
            args: TrainingArguments,
            state: TrainerState,
            control: TrainerControl,
            **kwargs,
        ):
            # Skip - the backend calls on_train_begin with full context
            pass

        def on_log(
            self,
            args: TrainingArguments,
            state: TrainerState,
            control: TrainerControl,
            logs: dict[str, Any] | None = None,
            **kwargs,
        ):
            # on_log is called when metrics are actually logged
            metrics = logs or {}

            # Skip non-training logs (e.g., eval logs)
            if "reward" not in metrics and "loss" not in metrics:
                return

            result = FinetuningIterationResult(
                iteration=state.global_step,
                reward_mean=metrics.get("reward", metrics.get("rewards/mean", 0.0)),
                reward_std=metrics.get("reward_std", metrics.get("rewards/std", 0.0)),
                kl_divergence=metrics.get("kl", metrics.get("objective/kl", 0.0)),
                policy_loss=metrics.get("loss", metrics.get("objective/loss", 0.0)),
                learning_rate=metrics.get("learning_rate", 0.0),
                total_time_sec=metrics.get("step_time", 0.0),
            )

            self._konic.on_iteration_end(result)

            if self._konic.should_stop_early(result):
                control.should_training_stop = True

        def on_save(
            self,
            args: TrainingArguments,
            state: TrainerState,
            control: TrainerControl,
            **kwargs,
        ):
            checkpoint_path = f"{args.output_dir}/checkpoint-{state.global_step}"
            self._konic.on_checkpoint_saved(checkpoint_path, state.global_step)

        def on_train_end(
            self,
            args: TrainingArguments,
            state: TrainerState,
            control: TrainerControl,
            **kwargs,
        ):
            # Skip - the backend calls on_train_end with full result
            pass

    return TRLCallbackAdapter(konic_callback)

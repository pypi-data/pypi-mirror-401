"""TRL DPO (Direct Preference Optimization) backend."""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from konic.common.errors import KonicValidationError
from konic.finetuning.backends.result import FinetuningResult
from konic.finetuning.backends.trl.adapter import (
    create_trl_callback_adapter,
    lora_config_to_peft_config,
    training_config_to_dpo_config,
)
from konic.finetuning.backends.trl.base import BaseTRLBackend, require_trl

logger = logging.getLogger(__name__)


class TRLDPOBackend(BaseTRLBackend):
    """TRL DPO backend for Direct Preference Optimization.

    DPO is an offline method that learns directly from preference pairs
    (chosen vs rejected responses) without requiring online generation
    or a reward model during training.

    Requires PreferenceDatasetConfig with chosen/rejected columns.
    Does NOT require a reward_composer (preferences are in the dataset).
    """

    def _validate_config(self) -> None:
        from konic.finetuning.dataset import PreferenceDatasetConfig

        if not isinstance(self.config.dataset_config, PreferenceDatasetConfig):
            raise KonicValidationError(
                "DPO requires PreferenceDatasetConfig with chosen/rejected columns. "
                "Use DatasetConfig(name='dataset', chosen_column='chosen', rejected_column='rejected').",
                field="dataset_config",
            )

    def _create_trainer(self) -> None:
        require_trl()
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from trl import DPOTrainer  # type: ignore[attr-defined]

        from konic.finetuning.dataset import DatasetLoader

        # Load dataset (must be preference format)
        dataset_loader = DatasetLoader(self.config.dataset_config)
        dataset = dataset_loader.load()

        # Configure output directory
        output_dir = self.config.checkpoint_dir or "./dpo_output"
        os.makedirs(output_dir, exist_ok=True)

        # Build DPO config
        dpo_config = training_config_to_dpo_config(
            self.config.training_config,
            output_dir=output_dir,
            max_steps=100,  # Will be overridden in train()
        )

        # Load model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            device_map=self.config.device,
        )
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Create TRL callback adapter
        trl_callback = create_trl_callback_adapter(self.config.callback)

        # Initialize trainer
        self._trainer = DPOTrainer(
            model=model,
            args=dpo_config,
            train_dataset=dataset,
            processing_class=tokenizer,
            peft_config=lora_config_to_peft_config(self.config.lora_config),
            callbacks=[trl_callback],
        )

        logger.info(f"Created DPOTrainer for {self.config.model_name}")

    def train(self, max_iterations: int, save_every: int | None = None) -> FinetuningResult:
        if self._trainer is None:
            raise KonicValidationError(
                "Trainer not initialized. Call setup() first.",
                field="trainer",
            )

        # Update max_steps
        self._trainer.args.max_steps = max_iterations
        if save_every:
            self._trainer.args.save_steps = save_every

        # Fire callback with full training config
        self.config.callback.on_train_begin(
            {
                "model_name": self.config.model_name,
                "method": "TRL_DPO",
                "max_iterations": max_iterations,
                "backend": self.name,
                "learning_rate": self.config.training_config.learning_rate,
                "batch_size": self.config.training_config.batch_size,
                "use_lora": self.config.lora_config is not None,
            }
        )

        # Run training
        start_time = time.time()
        try:
            self._trainer.train()
        except KeyboardInterrupt:
            logger.warning(
                "Training interrupted by user at step %d. Saving checkpoint...",
                self._trainer.state.global_step,
            )
            self._trainer.save_model(self._trainer.args.output_dir)
            self.config.callback.on_checkpoint_saved(
                self._trainer.args.output_dir, self._trainer.state.global_step
            )
        total_time = time.time() - start_time

        # Build result
        output_dir = self._trainer.args.output_dir
        result = FinetuningResult(
            total_iterations=self._trainer.state.global_step,
            model_name=self.config.model_name,
            model_path=output_dir,
            lora_config=self.config.lora_config.to_dict() if self.config.lora_config else None,
            training_config=self.config.training_config.to_dict(),
            total_time_sec=total_time,
        )

        # Extract metrics from training history
        best_loss = float("inf")
        best_step = 0
        if self._trainer.state.log_history:
            for log_entry in self._trainer.state.log_history:
                if "loss" in log_entry:
                    loss = log_entry["loss"]
                    step = log_entry.get("step", 0)
                    if loss < best_loss:
                        best_loss = loss
                        best_step = step

            # DPO reward = -loss (negated loss)
            # Lower DPO loss indicates better preference alignment, so we negate
            # to produce higher rewards for better models. See FinetuningResult
            # docstring for reward semantics across different backends.
            if best_loss < float("inf"):
                result.best_reward = -best_loss
                result.best_iteration = best_step

            # Get final metrics (also negated)
            for log_entry in reversed(self._trainer.state.log_history):
                if "loss" in log_entry:
                    result.final_reward_mean = -log_entry["loss"]
                    break

        # Extract KL divergence if available (DPO logs this as 'objective/kl' or 'kl')
        if self._trainer.state.log_history:
            for log_entry in reversed(self._trainer.state.log_history):
                kl = log_entry.get("kl", log_entry.get("objective/kl"))
                if kl is not None:
                    result.final_kl_divergence = kl
                    break

        # Save final model
        self._trainer.save_model(output_dir)
        self.config.callback.on_checkpoint_saved(output_dir, result.total_iterations)

        self.config.callback.on_train_end(result)
        return result

    def evaluate(self, prompts: list[str]) -> dict[str, Any]:
        """Evaluate model using DPO trainer's generation capabilities.

        Note: DPO doesn't use a reward model during training, so evaluation
        only returns generated responses without reward scores unless a
        reward_composer was provided.
        """
        return super().evaluate(prompts)

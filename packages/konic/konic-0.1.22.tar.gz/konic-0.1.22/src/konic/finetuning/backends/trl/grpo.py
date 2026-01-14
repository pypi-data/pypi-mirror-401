"""TRL GRPO (Group Relative Policy Optimization) backend."""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from konic.common.errors import KonicValidationError
from konic.finetuning.backends.result import FinetuningResult
from konic.finetuning.backends.trl.adapter import (
    adapt_reward_composer_to_trl,
    create_trl_callback_adapter,
    lora_config_to_peft_config,
    training_config_to_grpo_config,
)
from konic.finetuning.backends.trl.base import BaseTRLBackend, require_trl

logger = logging.getLogger(__name__)


class TRLGRPOBackend(BaseTRLBackend):
    """TRL GRPO backend for Group Relative Policy Optimization.

    GRPO is a modern RL method that doesn't require a separate value model,
    making it simpler and more efficient than classic PPO while achieving
    comparable or better results.

    Requires reward composer with @llm_reward decorated methods.
    """

    def _validate_config(self) -> None:
        if self.config.reward_composer is None:
            raise KonicValidationError(
                "GRPO requires a reward_composer to compute rewards during training. "
                "Please provide a reward_composer with @llm_reward methods.",
                field="reward_composer",
            )

    def _create_trainer(self) -> None:
        require_trl()
        from trl import GRPOTrainer  # type: ignore[attr-defined]

        from konic.finetuning.dataset import DatasetLoader

        # Load dataset
        dataset_loader = DatasetLoader(self.config.dataset_config)
        dataset = dataset_loader.load()

        # TRL expects a "prompt" column - rename if needed
        prompt_col = self.config.dataset_config.prompt_column
        column_names = dataset.column_names or []
        if prompt_col != "prompt" and prompt_col in column_names:
            dataset = dataset.rename_column(prompt_col, "prompt")

        # Truncate prompts to prevent context overflow
        # GRPO needs bounded prompts - very long prompts cause numerical instability
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        max_prompt_tokens = self.config.generation_config.max_prompt_length
        truncation_count = 0

        def truncate_prompt(example):
            nonlocal truncation_count
            original_tokens = tokenizer.encode(example["prompt"], add_special_tokens=False)
            if len(original_tokens) > max_prompt_tokens:
                truncation_count += 1
                tokens = original_tokens[:max_prompt_tokens]
                example["prompt"] = tokenizer.decode(tokens, skip_special_tokens=True)
            return example

        dataset = dataset.map(truncate_prompt)

        if truncation_count > 0:
            logger.warning(
                f"Truncated {truncation_count} prompts to {max_prompt_tokens} tokens. "
                f"Adjust generation_config.max_prompt_length to change this limit."
            )

        # Configure output directory
        output_dir = self.config.checkpoint_dir or "./grpo_output"
        os.makedirs(output_dir, exist_ok=True)

        # Build GRPO config
        grpo_config = training_config_to_grpo_config(
            self.config.training_config,
            generation_config=self.config.generation_config,
            output_dir=output_dir,
            max_steps=100,  # Will be overridden in train()
        )

        # Adapt reward composer (validated in _validate_config)
        assert self.config.reward_composer is not None
        reward_func = adapt_reward_composer_to_trl(self.config.reward_composer)

        # Create TRL callback adapter
        trl_callback = create_trl_callback_adapter(self.config.callback)

        # Initialize trainer
        self._trainer = GRPOTrainer(
            model=self.config.model_name,
            reward_funcs=reward_func,
            args=grpo_config,
            train_dataset=dataset,
            peft_config=lora_config_to_peft_config(self.config.lora_config),
            callbacks=[trl_callback],
        )

        logger.info(f"Created GRPOTrainer for {self.config.model_name}")

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
                "method": "TRL_GRPO",
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

        # Extract final reward from training history
        if self._trainer.state.log_history:
            # Find last entry with reward metric
            for log_entry in reversed(self._trainer.state.log_history):
                if "reward" in log_entry:
                    result.final_reward_mean = log_entry["reward"]
                    result.best_reward = log_entry["reward"]
                    result.best_iteration = log_entry.get("step", self._trainer.state.global_step)
                    if "kl" in log_entry:
                        result.final_kl_divergence = log_entry["kl"]
                    break

        # Save final model
        self._trainer.save_model(output_dir)
        self.config.callback.on_checkpoint_saved(output_dir, result.total_iterations)

        self.config.callback.on_train_end(result)
        return result

    def evaluate(self, prompts: list[str]) -> dict[str, Any]:
        """Evaluate model using GRPO trainer's generation capabilities."""
        return super().evaluate(prompts)

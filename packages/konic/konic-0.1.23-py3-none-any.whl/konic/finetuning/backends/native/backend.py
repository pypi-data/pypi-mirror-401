"""Native RLHF training backend using Konic's PPO implementation."""

from __future__ import annotations

import logging
import os
import time
from typing import TYPE_CHECKING, Any

import torch

from konic.common.errors import KonicRuntimeError, KonicValidationError
from konic.finetuning.backends.base import BackendConfig, BaseTrainingBackend
from konic.finetuning.backends.native.advantage import ADVANTAGE_STD_THRESHOLD
from konic.finetuning.backends.native.ppo import PPOUpdater
from konic.finetuning.backends.result import FinetuningIterationResult, FinetuningResult
from konic.finetuning.config import GenerationConfig, TrainingConfig
from konic.finetuning.dataset import DatasetLoader
from konic.finetuning.module import KonicTorchRLHF

if TYPE_CHECKING:
    from konic.finetuning.reward import BaseKonicLLMRewardComposer

logger = logging.getLogger(__name__)

# Re-export for backward compatibility
__all__ = ["NativeRLHFBackend", "ADVANTAGE_STD_THRESHOLD"]


class NativeRLHFBackend(BaseTrainingBackend):
    """Native PPO-based RLHF training backend.

    This is Konic's custom implementation providing fine-grained control
    over the PPO training loop with GAE, gradient accumulation, and KL penalty.
    """

    def __init__(self) -> None:
        self._config: BackendConfig | None = None
        self._module: KonicTorchRLHF | None = None
        self._dataset_loader: DatasetLoader | None = None
        self._optimizer: torch.optim.Optimizer | None = None
        self._ppo_updater: PPOUpdater | None = None
        self._is_setup = False

    @property
    def is_setup(self) -> bool:
        return self._is_setup

    @property
    def module(self) -> KonicTorchRLHF:
        if self._module is None:
            raise KonicRuntimeError(
                "Module not initialized. Call setup() first.", operation="module_access"
            )
        return self._module

    @property
    def dataset_loader(self) -> DatasetLoader:
        if self._dataset_loader is None:
            raise KonicRuntimeError(
                "Dataset loader not initialized. Call setup() first.",
                operation="dataset_loader_access",
            )
        return self._dataset_loader

    @property
    def optimizer(self) -> torch.optim.Optimizer:
        if self._optimizer is None:
            raise KonicRuntimeError(
                "Optimizer not initialized. Call setup() first.", operation="optimizer_access"
            )
        return self._optimizer

    @property
    def config(self) -> BackendConfig:
        if self._config is None:
            raise KonicRuntimeError(
                "Backend not configured. Call setup() first.", operation="config_access"
            )
        return self._config

    @property
    def training_config(self) -> TrainingConfig:
        return self.config.training_config

    @property
    def generation_config(self) -> GenerationConfig:
        return self.config.generation_config

    @property
    def reward_composer(self) -> BaseKonicLLMRewardComposer:
        if self.config.reward_composer is None:
            raise KonicRuntimeError(
                "Reward composer required for native RLHF backend.",
                operation="reward_composer_access",
            )
        return self.config.reward_composer

    def setup(self, config: BackendConfig) -> None:
        if self._is_setup:
            return

        self._config = config
        self._validate_config(config)
        self._initialize_components(config)
        self._is_setup = True

    def _validate_config(self, config: BackendConfig) -> None:
        """Validate configuration before setup."""
        if config.training_config.batch_size <= 0:
            raise KonicValidationError(
                f"batch_size must be positive, got {config.training_config.batch_size}",
                field="batch_size",
            )

        if config.reward_composer is None:
            raise KonicValidationError(
                "reward_composer is required for native RLHF backend",
                field="reward_composer",
            )

    def _initialize_components(self, config: BackendConfig) -> None:
        """Initialize module, dataset loader, optimizer, and PPO updater."""
        self._module = KonicTorchRLHF(
            model_name=config.model_name,
            lora_config=config.lora_config,
            generation_config=config.generation_config,
            device=config.device,
        )
        self.module.setup()

        self._dataset_loader = DatasetLoader(config.dataset_config)
        self.dataset_loader.load()

        params = self.module.get_trainable_parameters()
        self._optimizer = torch.optim.AdamW(
            params,
            lr=config.training_config.learning_rate,
            weight_decay=config.training_config.weight_decay,
        )

        self._ppo_updater = PPOUpdater(
            module=self.module,
            optimizer=self.optimizer,
            training_config=config.training_config,
            device=config.device,
        )

        if config.checkpoint_dir:
            os.makedirs(config.checkpoint_dir, exist_ok=True)

    def train(self, max_iterations: int, save_every: int | None = None) -> FinetuningResult:
        result = FinetuningResult(
            total_iterations=0,
            model_name=self.config.model_name,
            lora_config=self.config.lora_config.to_dict() if self.config.lora_config else None,
            training_config=self.training_config.to_dict(),
        )

        self._fire_train_begin_callback(max_iterations)

        try:
            self._run_training_loop(result, max_iterations, save_every)
        except KeyboardInterrupt:
            print("\nTraining interrupted by user.")

        self._save_final_model(result)
        self.config.callback.on_train_end(result)
        return result

    def _fire_train_begin_callback(self, max_iterations: int) -> None:
        """Fire the on_train_begin callback."""
        train_config = {
            "model_name": self.config.model_name,
            "use_lora": self.config.lora_config is not None,
            "learning_rate": self.training_config.learning_rate,
            "batch_size": self.training_config.batch_size,
            "max_iterations": max_iterations,
            "kl_penalty_weight": self.training_config.kl_penalty_weight,
            "backend": self.name,
        }
        self.config.callback.on_train_begin(train_config)

    def _run_training_loop(
        self,
        result: FinetuningResult,
        max_iterations: int,
        save_every: int | None,
    ) -> None:
        """Execute the main training loop."""
        for iteration in range(1, max_iterations + 1):
            self.config.callback.on_iteration_begin(iteration)

            try:
                iter_result = self._train_iteration(iteration)
            except StopIteration:
                logger.info("Dataset exhausted, ending training")
                break

            result.add_iteration_result(iter_result)
            result.total_samples += self.training_config.batch_size

            self.config.callback.on_iteration_end(iter_result)

            if self.config.callback.should_stop_early(iter_result):
                break

            if save_every and iteration % save_every == 0:
                self._save_checkpoint(iteration)

    def _save_final_model(self, result: FinetuningResult) -> None:
        """Save the final model checkpoint."""
        if self.config.checkpoint_dir:
            final_path = os.path.join(self.config.checkpoint_dir, "final")
            self.module.save_pretrained(final_path)
            result.model_path = final_path
            self.config.callback.on_checkpoint_saved(final_path, result.total_iterations)

    def _train_iteration(self, iteration: int) -> FinetuningIterationResult:
        import statistics

        start_time = time.time()

        batch = next(
            self.dataset_loader.iter_batches(batch_size=self.training_config.samples_per_iteration)
        )
        prompts = self.dataset_loader.get_prompts(batch)

        if not prompts:
            raise KonicValidationError(
                "No prompts available from dataset. Check dataset configuration.",
                field="prompts",
            )

        gen_start = time.time()
        self.config.callback.on_generation_begin(prompts)
        responses, input_ids, response_ids = self._generate_responses(prompts)
        gen_time = time.time() - gen_start
        self.config.callback.on_generation_end(prompts, responses)

        reward_start = time.time()
        rewards, reward_breakdown = self._compute_rewards(prompts, responses)
        reward_time = time.time() - reward_start
        self.config.callback.on_reward_computed(rewards, reward_breakdown)

        update_start = time.time()
        losses = self._ppo_update(input_ids, response_ids, rewards)
        update_time = time.time() - update_start

        total_time = time.time() - start_time

        rewards_tensor = torch.tensor(rewards)
        response_lengths = [len(r.split()) for r in responses]

        return FinetuningIterationResult(
            iteration=iteration,
            reward_mean=rewards_tensor.mean().item(),
            reward_std=rewards_tensor.std().item() if len(rewards) > 1 else 0.0,
            reward_min=rewards_tensor.min().item(),
            reward_max=rewards_tensor.max().item(),
            kl_divergence=losses.get("kl_divergence", 0.0),
            policy_loss=losses.get("policy_loss", 0.0),
            value_loss=losses.get("value_loss", 0.0),
            entropy_loss=losses.get("entropy_loss", 0.0),
            total_loss=losses.get("total_loss", 0.0),
            response_length_mean=statistics.mean(response_lengths),
            response_length_std=(
                statistics.stdev(response_lengths) if len(response_lengths) > 1 else 0.0
            ),
            learning_rate=self.optimizer.param_groups[0]["lr"],
            clip_fraction=losses.get("clip_fraction", 0.0),
            approx_kl=losses.get("approx_kl", 0.0),
            reward_breakdown={k: statistics.mean(v) for k, v in reward_breakdown.items()},
            generation_time_sec=gen_time,
            reward_compute_time_sec=reward_time,
            update_time_sec=update_time,
            total_time_sec=total_time,
        )

    def _generate_responses(
        self, prompts: list[str]
    ) -> tuple[list[str], torch.Tensor, torch.Tensor]:
        tokenizer = self.module.tokenizer
        inputs = tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.generation_config.max_length,
        )
        input_ids: torch.Tensor = inputs["input_ids"].to(self.config.device)  # type: ignore[union-attr]
        attention_mask: torch.Tensor = inputs["attention_mask"].to(self.config.device)  # type: ignore[union-attr]

        with torch.no_grad():
            output_ids = self.module.generate(input_ids=input_ids, attention_mask=attention_mask)

        response_ids = output_ids[:, input_ids.shape[1] :]
        responses = tokenizer.batch_decode(response_ids, skip_special_tokens=True)
        return responses, input_ids, response_ids

    def _compute_rewards(
        self, prompts: list[str], responses: list[str]
    ) -> tuple[list[float], dict[str, list[float]]]:
        if hasattr(self.reward_composer, "compose_batch"):
            return self.reward_composer.compose_batch(prompts, responses)

        rewards = []
        breakdowns: dict[str, list[float]] = {}
        for prompt, response in zip(prompts, responses):
            reward = self.reward_composer.compose(prompt, response)
            rewards.append(reward)
            breakdown = self.reward_composer.get_reward_breakdown(prompt, response)
            for key, value in breakdown.items():
                if key not in breakdowns:
                    breakdowns[key] = []
                breakdowns[key].append(value)
        return rewards, breakdowns

    def _ppo_update(
        self,
        input_ids: torch.Tensor,
        response_ids: torch.Tensor,
        rewards: list[float],
    ) -> dict[str, float]:
        """Execute PPO update using the PPOUpdater."""
        batch_size = input_ids.size(0)
        if batch_size == 0:
            raise KonicValidationError(
                "Empty batch provided to PPO update",
                field="input_ids",
            )

        if len(rewards) != batch_size:
            raise KonicValidationError(
                f"Rewards length ({len(rewards)}) doesn't match batch size ({batch_size})",
                field="rewards",
            )

        if self._ppo_updater is None:
            raise KonicRuntimeError(
                "PPO updater not initialized. Call setup() first.",
                operation="ppo_update",
            )

        return self._ppo_updater.update(input_ids, response_ids, rewards)

    def _compute_advantages(
        self, rewards: torch.Tensor, values: torch.Tensor, gamma: float, gae_lambda: float
    ) -> torch.Tensor:
        """Compute GAE advantages (backward compatibility)."""
        from konic.finetuning.backends.native.advantage import compute_gae_advantages

        return compute_gae_advantages(rewards, values, gamma, gae_lambda)

    def _save_checkpoint(self, iteration: int) -> None:
        if not self.config.checkpoint_dir:
            return

        checkpoint_path = os.path.join(self.config.checkpoint_dir, f"checkpoint-{iteration}")
        self.module.save_pretrained(checkpoint_path)
        optimizer_path = os.path.join(checkpoint_path, "optimizer.pt")
        torch.save(self.optimizer.state_dict(), optimizer_path)
        self.config.callback.on_checkpoint_saved(checkpoint_path, iteration)

    def evaluate(self, prompts: list[str]) -> dict[str, Any]:
        responses, _, _ = self._generate_responses(prompts)
        rewards, breakdown = self._compute_rewards(prompts, responses)

        return {
            "prompts": prompts,
            "responses": responses,
            "rewards": rewards,
            "reward_mean": sum(rewards) / len(rewards),
            "reward_breakdown": breakdown,
        }

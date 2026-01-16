"""PPO (Proximal Policy Optimization) update logic."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import torch

from konic.finetuning.backends.native.advantage import (
    compute_gae_advantages,
    normalize_advantages,
)

if TYPE_CHECKING:
    from konic.finetuning.config import TrainingConfig
    from konic.finetuning.module import KonicTorchRLHF

logger = logging.getLogger(__name__)


@dataclass
class PPOUpdateResult:
    """Results from a PPO update step."""

    policy_loss: float
    value_loss: float
    entropy_loss: float
    total_loss: float
    clip_fraction: float
    approx_kl: float
    kl_divergence: float


class PPOUpdater:
    """Handles PPO optimization updates for RLHF training."""

    def __init__(
        self,
        module: KonicTorchRLHF,
        optimizer: torch.optim.Optimizer,
        training_config: TrainingConfig,
        device: str,
    ) -> None:
        self._module = module
        self._optimizer = optimizer
        self._config = training_config
        self._device = device

    def update(
        self,
        input_ids: torch.Tensor,
        response_ids: torch.Tensor,
        rewards: list[float],
    ) -> dict[str, float]:
        """Execute PPO update on a batch.

        Args:
            input_ids: Input token IDs.
            response_ids: Generated response token IDs.
            rewards: Reward values for each sample.

        Returns:
            Dictionary of loss and metric values.
        """
        batch_size = input_ids.size(0)
        accum_steps = self._get_accumulation_steps(batch_size)

        # Prepare sequences
        full_ids = torch.cat([input_ids, response_ids], dim=1)
        pad_token_id = self._module.tokenizer.pad_token_id or 0
        attention_mask: torch.Tensor = (full_ids != pad_token_id).to(torch.long)  # type: ignore[union-attr]

        # Compute old policy outputs
        old_outputs = self._compute_old_outputs(full_ids, attention_mask)

        # Compute advantages and returns
        advantages, returns = self._compute_advantages_and_returns(
            rewards, old_outputs, full_ids.shape[1], batch_size
        )

        # Run PPO epochs
        metrics = self._run_ppo_epochs(
            full_ids,
            attention_mask,
            advantages,
            returns,
            old_outputs,
            batch_size,
            accum_steps,
        )

        # Compute final KL metrics
        kl_divergence = (old_outputs["log_probs"] - old_outputs["ref_log_probs"]).mean().item()

        with torch.no_grad():
            final_outputs = self._module.forward_all(full_ids, attention_mask, compute_ref=False)
            approx_kl = (old_outputs["log_probs"] - final_outputs.log_probs).mean().item()

        return {
            **metrics,
            "approx_kl": approx_kl,
            "kl_divergence": kl_divergence,
        }

    def _get_accumulation_steps(self, batch_size: int) -> int:
        """Get effective gradient accumulation steps."""
        accum_steps = self._config.gradient_accumulation_steps

        if batch_size < accum_steps:
            logger.warning(
                f"Batch size ({batch_size}) < gradient_accumulation_steps ({accum_steps}). "
                f"Reducing accumulation to {batch_size}."
            )
            return batch_size

        return accum_steps

    def _compute_old_outputs(
        self, full_ids: torch.Tensor, attention_mask: torch.Tensor
    ) -> dict[str, torch.Tensor]:
        """Compute outputs from old policy (before update)."""
        with torch.no_grad():
            outputs = self._module.forward_all(full_ids, attention_mask, compute_ref=True)
            return {
                "log_probs": outputs.log_probs.detach(),
                "values": outputs.values.detach(),
                "ref_log_probs": outputs.ref_log_probs.detach(),
            }

    def _compute_advantages_and_returns(
        self,
        rewards: list[float],
        old_outputs: dict[str, torch.Tensor],
        seq_len: int,
        batch_size: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute GAE advantages and returns."""
        rewards_tensor = torch.tensor(rewards, device=self._device, dtype=torch.float32)
        reward_seq = torch.zeros(batch_size, seq_len, device=self._device)
        reward_seq[:, -1] = rewards_tensor

        # Apply KL penalty
        kl_penalty = self._config.kl_penalty_weight * (
            old_outputs["log_probs"] - old_outputs["ref_log_probs"]
        )
        adjusted_rewards = reward_seq[:, :-1] - kl_penalty

        # Compute GAE advantages
        advantages = compute_gae_advantages(
            adjusted_rewards,
            old_outputs["values"][:, :-1],
            self._config.gamma,
            self._config.gae_lambda,
        )

        # Normalize advantages
        advantages = normalize_advantages(advantages)

        # Compute returns
        returns = advantages + old_outputs["values"][:, :-1]

        return advantages, returns

    def _run_ppo_epochs(
        self,
        full_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        advantages: torch.Tensor,
        returns: torch.Tensor,
        old_outputs: dict[str, torch.Tensor],
        batch_size: int,
        accum_steps: int,
    ) -> dict[str, float]:
        """Run PPO optimization epochs."""
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_entropy_loss = 0.0
        clip_fractions: list[float] = []
        num_updates = 0

        use_amp = self._module.use_amp
        scaler = self._module.scaler

        for _ in range(self._config.ppo_epochs):
            self._optimizer.zero_grad()

            for accum_idx in range(accum_steps):
                losses = self._compute_micro_batch_loss(
                    full_ids,
                    attention_mask,
                    advantages,
                    returns,
                    old_outputs["log_probs"],
                    batch_size,
                    accum_steps,
                    accum_idx,
                )

                if losses is None:
                    continue

                # Backward pass
                if use_amp and scaler is not None:
                    scaler.scale(losses["scaled_loss"]).backward()
                else:
                    losses["scaled_loss"].backward()

                total_policy_loss += losses["policy_loss"]
                total_value_loss += losses["value_loss"]
                total_entropy_loss += losses["entropy_loss"]
                clip_fractions.append(losses["clip_fraction"])
                num_updates += 1

            # Optimizer step
            self._optimizer_step(use_amp, scaler)

        if num_updates == 0:
            return {
                "policy_loss": 0.0,
                "value_loss": 0.0,
                "entropy_loss": 0.0,
                "total_loss": 0.0,
                "clip_fraction": 0.0,
            }

        return {
            "policy_loss": total_policy_loss / num_updates,
            "value_loss": total_value_loss / num_updates,
            "entropy_loss": total_entropy_loss / num_updates,
            "total_loss": (total_policy_loss + total_value_loss + total_entropy_loss) / num_updates,
            "clip_fraction": sum(clip_fractions) / len(clip_fractions),
        }

    def _compute_micro_batch_loss(
        self,
        full_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        advantages: torch.Tensor,
        returns: torch.Tensor,
        old_log_probs: torch.Tensor,
        batch_size: int,
        accum_steps: int,
        accum_idx: int,
    ) -> dict[str, Any] | None:
        """Compute loss for a micro-batch."""
        micro_batch_size = math.ceil(batch_size / accum_steps)
        start = accum_idx * micro_batch_size
        end = min(start + micro_batch_size, batch_size)
        actual_micro_size = end - start

        if actual_micro_size == 0:
            return None

        # Slice micro-batch
        mb_ids = full_ids[start:end]
        mb_mask = attention_mask[start:end]
        mb_advantages = advantages[start:end]
        mb_old_log_probs = old_log_probs[start:end]
        mb_returns = returns[start:end]

        with self._module.get_amp_context():
            new_outputs = self._module.forward_all(mb_ids, mb_mask, compute_ref=False)
            new_log_probs = new_outputs.log_probs
            new_values = new_outputs.values

            # Policy loss (clipped surrogate objective)
            ratio = torch.exp(new_log_probs - mb_old_log_probs)
            clip_ratio = torch.clamp(
                ratio,
                1.0 - self._config.clip_ratio,
                1.0 + self._config.clip_ratio,
            )
            policy_loss = -torch.min(ratio * mb_advantages, clip_ratio * mb_advantages).mean()

            # Value loss
            value_loss = 0.5 * ((new_values[:, :-1] - mb_returns) ** 2).mean()

            # Entropy loss
            entropy = -new_log_probs.mean()
            entropy_loss = -self._config.entropy_coef * entropy

            # Combined loss
            loss = policy_loss + self._config.vf_coef * value_loss + entropy_loss
            scaled_loss = loss * (actual_micro_size / batch_size)

            # Clip fraction for logging
            clip_fraction = ((ratio - 1.0).abs() > self._config.clip_ratio).float().mean().item()

        return {
            "scaled_loss": scaled_loss,
            "policy_loss": policy_loss.item(),
            "value_loss": value_loss.item(),
            "entropy_loss": entropy_loss.item(),
            "clip_fraction": clip_fraction,
        }

    def _optimizer_step(self, use_amp: bool, scaler: Any | None) -> None:
        """Execute optimizer step with optional AMP."""
        if use_amp and scaler is not None:
            scaler.unscale_(self._optimizer)
            torch.nn.utils.clip_grad_norm_(
                self._module.get_trainable_parameters(),
                self._config.max_grad_norm,
            )
            scaler.step(self._optimizer)
            scaler.update()
        else:
            torch.nn.utils.clip_grad_norm_(
                self._module.get_trainable_parameters(),
                self._config.max_grad_norm,
            )
            self._optimizer.step()

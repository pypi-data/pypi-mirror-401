"""Generalized Advantage Estimation (GAE) for PPO training."""

from __future__ import annotations

import torch

ADVANTAGE_STD_THRESHOLD = 1e-6


def compute_gae_advantages(
    rewards: torch.Tensor,
    values: torch.Tensor,
    gamma: float,
    gae_lambda: float,
) -> torch.Tensor:
    """Compute Generalized Advantage Estimation (GAE).

    GAE provides a balance between bias and variance in advantage estimation
    by exponentially weighting TD residuals.

    Args:
        rewards: Reward tensor of shape (batch_size, seq_len).
        values: Value estimates of shape (batch_size, seq_len).
        gamma: Discount factor for future rewards.
        gae_lambda: GAE lambda for bias-variance tradeoff.

    Returns:
        Advantage tensor of shape (batch_size, seq_len).
    """
    advantages = torch.zeros_like(rewards)
    last_gae = 0

    for t in reversed(range(rewards.shape[1])):
        if t == rewards.shape[1] - 1:
            next_value = 0
        else:
            next_value = values[:, t + 1]

        delta = rewards[:, t] + gamma * next_value - values[:, t]
        advantages[:, t] = last_gae = delta + gamma * gae_lambda * last_gae

    return advantages


def normalize_advantages(
    advantages: torch.Tensor,
    threshold: float = ADVANTAGE_STD_THRESHOLD,
) -> torch.Tensor:
    """Normalize advantages for stable training.

    Args:
        advantages: Raw advantage estimates.
        threshold: Minimum std to avoid division by zero.

    Returns:
        Normalized advantages (zero mean, unit variance if std > threshold).
    """
    mean = advantages.mean()
    std = advantages.std()

    if std > threshold:
        return (advantages - mean) / std
    return advantages - mean

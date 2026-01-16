# TRL GRPO Finetuning Example

This example demonstrates how to use Konic's TRL backend with **Group Relative Policy Optimization (GRPO)** for RLHF training.

## What is GRPO?

GRPO (Group Relative Policy Optimization) is an alternative to PPO for RLHF that:

- **No value head required**: Simpler model architecture
- **Relative rewards**: Compares multiple generations per prompt instead of absolute rewards
- **Faster convergence**: Often achieves good results faster for reward optimization tasks

## Files

- `grpo_sentiment.py` - Main example demonstrating TRL GRPO for sentiment-guided generation

## Running the Example

```bash
python grpo_sentiment.py
```

## Key Differences from Native PPO

| Aspect         | Native PPO                   | TRL GRPO                      |
| -------------- | ---------------------------- | ----------------------------- |
| Value Head     | Required                     | Not required                  |
| Reward Type    | Absolute                     | Relative (group-based)        |
| Training Style | Single generation per prompt | Multiple generations compared |
| Implementation | Konic native                 | TRL library                   |

## Configuration

To use TRL GRPO, simply set the `method` parameter:

```python
from konic.finetuning import KonicFinetuningEngine, KonicFinetuningMethodType

engine = KonicFinetuningEngine(
    model_name="gpt2",
    reward_composer=my_reward_composer,
    dataset_config=dataset_config,
    method=KonicFinetuningMethodType.TRL_GRPO,  # Use TRL GRPO
)
```

## Other Available Methods

- `KonicFinetuningMethodType.NATIVE_PPO` - Explicit native PPO
- `KonicFinetuningMethodType.TRL_GRPO` - TRL Group Relative Policy Optimization
- `KonicFinetuningMethodType.TRL_DPO` - TRL Direct Preference Optimization (requires preference dataset)

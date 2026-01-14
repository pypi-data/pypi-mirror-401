# Minimal TRL GRPO Example

The simplest possible example of using Konic's TRL GRPO backend for RLHF finetuning.

## Overview

This example demonstrates TRL GRPO in ~60 lines of code:
- Custom reward function using `@llm_reward` decorator
- TRL GRPO backend selection via `method=KonicFinetuningMethodType.TRL_GRPO`
- Basic training and evaluation

## Requirements

```bash
pip install konic
```

## Usage

```bash
python examples/finetuning/trl_basic/trl_basic.py
```

## What it does

1. Creates a simple reward function that prefers longer, non-repetitive responses
2. Loads IMDB dataset (20 samples for quick demo)
3. Trains GPT-2 using TRL GRPO for 5 iterations
4. Evaluates with a test prompt

## Expected Output

```
Backend: TRLGRPOBackend
...
Best Reward: ~0.90 (iteration 5)
Test: 'The movie was' -> '...'
```

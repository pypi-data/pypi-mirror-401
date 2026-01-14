#!/usr/bin/env python3
"""Run Finetuning Basic Template Locally.

This script provides a complete local execution of the finetuning_basic boilerplate
template without requiring Konic Cloud deployment.

The finetuning_basic template demonstrates:
- Simple reward composer with brevity and coherence rewards
- Minimal LoRA configuration for parameter-efficient training
- HuggingFace IMDB dataset for training prompts
- GPT-2 as base model (small, fast for demonstration)

Usage:
    # Default settings (50 iterations, GPT-2, IMDB dataset)
    python run_basic_template.py

    # Custom iterations
    python run_basic_template.py --iterations 100

    # Different model
    python run_basic_template.py --model gpt2-medium

    # Save checkpoints
    python run_basic_template.py --save-every 10 --output-dir ./my_model

    # CPU-only training
    python run_basic_template.py --device cpu

    # Force MPS (Apple Silicon)
    python run_basic_template.py --device mps
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

import torch

from konic.finetuning import (
    DatasetConfig,
    DatasetSource,
    KonicFinetuningAgent,
    KonicFinetuningCallback,
    KonicFinetuningEngine,
    KonicLLMRewardComposer,
    LoraConfig,
    TrainingConfig,
    llm_reward,
)

if TYPE_CHECKING:
    from konic.finetuning.engine import FinetuningIterationResult, FinetuningResult

# =============================================================================
# Reward Composer (from finetuning_basic template)
# =============================================================================


class SimpleRewardComposer(KonicLLMRewardComposer):
    """Simple reward composer with basic reward signals.

    This composer provides two reward functions:
    - brevity_bonus: Rewards shorter, more concise responses
    - coherence_reward: Penalizes repetitive text patterns
    """

    @llm_reward
    def brevity_bonus(self, prompt: str, response: str) -> float:
        """Reward shorter, more concise responses."""
        max_length = 300
        response_length = len(response)

        if response_length >= max_length:
            return 0.0

        return max(0.0, 1.0 - (response_length / max_length))

    @llm_reward
    def coherence_reward(self, prompt: str, response: str) -> float:
        """Penalize repetitive patterns in the response."""
        if not response:
            return 1.0

        words = response.lower().split()

        if len(words) < 2:
            return 1.0

        # Check for consecutive repeated words
        repeated_words = sum(1 for i in range(1, len(words)) if words[i] == words[i - 1])
        repetition_ratio = repeated_words / len(words)

        return max(0.0, 1.0 - repetition_ratio * 2)


# =============================================================================
# Verbose Training Callback
# =============================================================================


class VerboseTrainingCallback(KonicFinetuningCallback):
    """Enhanced callback with detailed per-iteration logging."""

    def __init__(self, log_samples: bool = True, log_rewards: bool = True):
        super().__init__(
            log_interval=1,
            log_samples=log_samples,
            max_samples_to_log=2,
            use_mlflow=False,
            verbose=True,
        )
        self.log_rewards = log_rewards
        self._iteration_start_time = 0.0
        self._full_prompts: list[str] = []
        self._full_responses: list[str] = []

    def on_iteration_begin(self, iteration: int) -> None:
        self._iteration_start_time = time.time()
        print(f"\n{'─' * 60}")
        print(f"  Iteration {iteration}")
        print(f"{'─' * 60}")

    def on_generation_begin(self, prompts: list[str]) -> None:
        print(f"  [Generate] Processing {len(prompts)} prompts...")

    def on_generation_end(self, prompts: list[str], responses: list[str]) -> None:
        super().on_generation_end(prompts, responses)
        if responses:
            avg_len = statistics.mean(len(r) for r in responses)
            print(f"  [Generate] Done. Avg response length: {avg_len:.0f} chars")

        # Store full prompts/responses for logging after rewards
        self._full_prompts = prompts[: self.max_samples_to_log]
        self._full_responses = responses[: self.max_samples_to_log]

    def on_reward_computed(
        self,
        rewards: list[float],
        reward_breakdown: dict[str, list[float]],
    ) -> None:
        if not rewards:
            return

        reward_mean = statistics.mean(rewards)
        reward_std = statistics.stdev(rewards) if len(rewards) > 1 else 0.0
        print(f"  [Reward]   Mean: {reward_mean:.4f} (±{reward_std:.4f})")

        if self.log_rewards and reward_breakdown:
            for name, values in reward_breakdown.items():
                avg_val = statistics.mean(values)
                print(f"             └─ {name}: {avg_val:.4f}")

        # Log generated samples with their individual rewards
        if hasattr(self, "_full_prompts") and self._full_prompts:
            print(f"\n  {'─' * 56}")
            print("  Generated Samples:")
            print(f"  {'─' * 56}")
            for i, (prompt, response) in enumerate(zip(self._full_prompts, self._full_responses)):
                sample_reward = rewards[i] if i < len(rewards) else 0.0
                # Truncate prompt for display
                prompt_display = prompt[:80] + "..." if len(prompt) > 80 else prompt
                print(f"  [Sample {i + 1}] Reward: {sample_reward:.4f}")
                print(f'    Prompt:   "{prompt_display}"')
                print(f'    Response: "{response}"')
                # Show individual reward breakdown for this sample
                if reward_breakdown:
                    breakdown_str = " | ".join(
                        f"{k}: {v[i]:.3f}" for k, v in reward_breakdown.items() if i < len(v)
                    )
                    print(f"    Breakdown: {breakdown_str}")
                print()
            print(f"  {'─' * 56}")

    def on_iteration_end(self, result: FinetuningIterationResult) -> None:
        elapsed = time.time() - self._iteration_start_time

        print(
            f"  [PPO]      Policy Loss: {result.policy_loss:.4f} | "
            f"Value Loss: {result.value_loss:.4f}"
        )
        print(
            f"  [PPO]      KL Div: {result.kl_divergence:.4f} | "
            f"Clip Frac: {result.clip_fraction:.2%}"
        )
        print(
            f"  [Time]     Gen: {result.generation_time_sec:.2f}s | "
            f"Reward: {result.reward_compute_time_sec:.2f}s | "
            f"Update: {result.update_time_sec:.2f}s | "
            f"Total: {elapsed:.2f}s"
        )

    def on_checkpoint_saved(self, path: str, iteration: int) -> None:
        print(f"\n  [Checkpoint] Saved to: {path}")


# =============================================================================
# Device Detection
# =============================================================================


def get_best_device(preferred: str | None = None) -> str:
    """Detect the best available device for training.

    Priority: user preference > CUDA > MPS (Apple Silicon) > CPU
    """
    if preferred:
        # User explicitly specified a device
        if preferred == "mps" and not torch.backends.mps.is_available():
            print("WARNING: MPS requested but not available. Falling back to CPU.")
            return "cpu"
        if preferred == "cuda" and not torch.cuda.is_available():
            print("WARNING: CUDA requested but not available. Falling back to CPU.")
            return "cpu"
        return preferred

    # Auto-detect best device
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def print_device_info(device: str) -> None:
    """Print information about the selected device."""
    print("\nDevice Information:")
    print(f"  Selected: {device}")

    if device == "cuda":
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        mem_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"  Memory: {mem_gb:.1f} GB")
    elif device == "mps":
        print("  Backend: Apple Metal Performance Shaders")
        print("  Note: MPS acceleration enabled for Apple Silicon")
    else:
        print("  Note: Running on CPU (slower training)")
    print()


# =============================================================================
# Agent Creation
# =============================================================================


def create_agent(
    model_name: str = "gpt2",
    max_samples: int = 500,
    batch_size: int = 4,
    learning_rate: float = 5e-5,
) -> KonicFinetuningAgent:
    """Create finetuning agent with basic template configuration."""
    # LoRA configuration for parameter-efficient finetuning
    lora_config = LoraConfig(
        r=8,  # Low rank for efficiency
        lora_alpha=16,  # Scaling factor
        lora_dropout=0.1,
        target_modules=["c_attn", "c_proj"],  # GPT-2 attention modules
    )

    # Training hyperparameters
    training_config = TrainingConfig(
        learning_rate=learning_rate,
        batch_size=batch_size,
        gradient_accumulation_steps=2,
        kl_penalty_weight=0.05,
    )

    # Dataset configuration
    dataset_config = DatasetConfig(
        source=DatasetSource.HUGGINGFACE,
        name="imdb",
        prompt_column="text",
        split="train",
        max_samples=max_samples,
        shuffle=True,
    )

    # Create the finetuning agent
    return KonicFinetuningAgent(
        base_model=model_name,
        reward_composer=SimpleRewardComposer(),
        lora_config=lora_config,
        dataset_config=dataset_config,
        training_config=training_config,
    )


# =============================================================================
# Training Execution
# =============================================================================


def run_training(
    agent: KonicFinetuningAgent,
    iterations: int,
    save_every: int | None,
    output_dir: Path,
    device: str,
    verbose: bool = True,
) -> tuple[FinetuningResult, KonicFinetuningEngine]:
    """Run the RLHF training loop."""
    # Create verbose callback
    callback = VerboseTrainingCallback(log_samples=True, log_rewards=True) if verbose else None

    # Create engine from agent with custom callback
    print("Initializing finetuning engine...")
    engine = KonicFinetuningEngine.from_agent(agent)

    # Set checkpoint directory and device
    engine.checkpoint_dir = str(output_dir)
    engine.device = device

    # Attach custom callback
    if callback:
        engine.callback = callback

    # Print training info
    print("\n" + "=" * 60)
    print("Starting RLHF Training")
    print("=" * 60)
    print(f"  Model:          {agent.get_base_model()}")
    print(f"  Device:         {device}")
    print(f"  Iterations:     {iterations}")
    print(f"  Batch Size:     {agent.get_training_config().batch_size}")
    print(f"  Learning Rate:  {agent.get_training_config().learning_rate}")
    print(f"  KL Penalty:     {agent.get_training_config().kl_penalty_weight}")

    lora = agent.get_lora_config()
    if lora is not None:
        print(f"  LoRA Rank:      {lora.r}")
        print(f"  LoRA Alpha:     {lora.lora_alpha}")
        print(f"  Target Modules: {lora.target_modules}")
    print("=" * 60)

    start_time = time.time()

    result = engine.train(
        max_iterations=iterations,
        save_every=save_every,
    )

    total_time = time.time() - start_time

    # Print final summary
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"  Total Iterations: {result.total_iterations}")
    print(f"  Total Time:       {total_time:.1f} seconds")
    print(f"  Best Reward:      {result.best_reward:.4f} (iter {result.best_iteration})")
    print(f"  Final Reward:     {result.final_reward_mean:.4f}")
    print(f"  Final KL Div:     {result.final_kl_divergence:.4f}")
    print(f"  Model Path:       {result.model_path}")
    print("=" * 60)

    return result, engine


def run_evaluation(engine: KonicFinetuningEngine, test_prompts: list[str]) -> None:
    """Evaluate the trained model on test prompts."""
    print("\n" + "=" * 60)
    print("Evaluating Trained Model")
    print("=" * 60)

    eval_results = engine.evaluate(test_prompts)

    for prompt, response, reward in zip(
        eval_results["prompts"],
        eval_results["responses"],
        eval_results["rewards"],
    ):
        print(f"\nPrompt: {prompt}")
        print(f"Response: {response[:200]}...")
        print(f"Reward: {reward:.3f}")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Finetuning Basic Template Locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_basic_template.py
    python run_basic_template.py --iterations 100
    python run_basic_template.py --model gpt2-medium --batch-size 2
    python run_basic_template.py --save-every 10 --output-dir ./my_model
        """,
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gpt2",
        help="Base model name (default: gpt2)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=50,
        help="Number of training iterations (default: 50)",
    )
    parser.add_argument(
        "--save-every",
        type=int,
        default=None,
        help="Save checkpoint every N iterations (default: final only)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./finetuning_basic_output"),
        help="Directory to save model checkpoints",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=500,
        help="Maximum samples from dataset (default: 500)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Training batch size (default: 4)",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=5e-5,
        help="Learning rate (default: 5e-5)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device to use (cpu, cuda, cuda:0, etc). Auto-detected if not set.",
    )
    parser.add_argument(
        "--skip-eval",
        action="store_true",
        help="Skip evaluation after training",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Detect best device
    device = get_best_device(args.device)

    # Print banner
    print("=" * 60)
    print("Konic Finetuning Basic Template - Local Runner")
    print("=" * 60)
    print()
    print("Configuration:")
    print(f"  Model:        {args.model}")
    print(f"  Iterations:   {args.iterations}")
    print(f"  Batch Size:   {args.batch_size}")
    print(f"  Max Samples:  {args.max_samples}")
    print(f"  Learning Rate:{args.learning_rate}")
    print(f"  Save Every:   {args.save_every or 'final only'}")
    print(f"  Output Dir:   {args.output_dir}")

    # Print device info
    print_device_info(device)

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Create agent
        print("Creating finetuning agent...")
        agent = create_agent(
            model_name=args.model,
            max_samples=args.max_samples,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
        )
        print(f"[OK] Agent created with {agent.get_base_model()}")

        # Run training with verbose logging
        result, engine = run_training(
            agent=agent,
            iterations=args.iterations,
            save_every=args.save_every,
            output_dir=args.output_dir,
            device=device,
            verbose=True,
        )

        # Run evaluation
        if not args.skip_eval:
            test_prompts = [
                "The movie was",
                "I really think that this film",
                "Overall, my experience was",
            ]
            run_evaluation(engine, test_prompts)

        print("\n" + "=" * 60)
        print("Finetuning Basic Template - Complete!")
        print("=" * 60)

        return 0

    except ImportError as e:
        print(f"ERROR: Missing dependency - {e}")
        print("\nInstall required dependencies with:")
        print("  pip install konic[finetuning]")
        print("\nOr for full development setup:")
        print("  pip install transformers peft datasets accelerate torch")
        return 1

    except Exception as e:
        print(f"ERROR: Training failed - {e}")
        raise


if __name__ == "__main__":
    sys.exit(main())

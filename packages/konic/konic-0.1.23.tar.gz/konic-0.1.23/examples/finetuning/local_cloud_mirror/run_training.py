#!/usr/bin/env python3
"""Local Training Script - Mirrors Konic Cloud Platform Training Process.

This script replicates the training execution flow from the konic-platform
train container (train/main.py) for local development and testing.

Cloud Platform Flow Replicated:
1. Load agent from file path (like downloading from presigned URL)
2. Detect agent type (finetuning vs traditional RL)
3. Initialize engine from agent configuration
4. Run training with iteration logging
5. Save checkpoints and final model
6. Optional: Log metrics to local MLflow or file

Environment Variables (matching cloud container):
- AGENT_PATH: Path to agent.py file (required)
- ITERATIONS: Number of training iterations (default: 100)
- CHECKPOINT_INTERVAL: Save every N iterations, 0=final only (default: 0)
- CHECKPOINT_DIR: Where to save checkpoints (default: ./checkpoints)
- USE_MLFLOW: Enable MLflow logging (default: false)
- MLFLOW_TRACKING_URI: MLflow server URI (default: ./mlruns)

Usage:
    # Basic usage
    python run_training.py --agent-path /path/to/agent.py

    # With environment variables (cloud-style)
    AGENT_PATH=./my_agent.py ITERATIONS=50 python run_training.py

    # With CLI arguments
    python run_training.py --agent-path ./agent.py --iterations 50 --checkpoint-interval 10

    # With MLflow tracking
    python run_training.py --agent-path ./agent.py --use-mlflow
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import torch

if TYPE_CHECKING:
    from konic.finetuning import KonicFinetuningAgent
    from konic.finetuning.engine import FinetuningIterationResult


@dataclass
class TrainingConfig:
    """Configuration for local training run."""

    agent_path: Path
    iterations: int = 100
    checkpoint_interval: int = 0
    checkpoint_dir: Path = Path("./checkpoints")
    use_mlflow: bool = False
    mlflow_tracking_uri: str = "./mlruns"
    verbose: bool = True
    device: str | None = None


# =============================================================================
# Device Detection
# =============================================================================


def get_best_device(preferred: str | None = None) -> str:
    """Detect the best available device for training.

    Priority: user preference > CUDA > MPS (Apple Silicon) > CPU
    """
    if preferred:
        if preferred == "mps" and not torch.backends.mps.is_available():
            print("WARNING: MPS requested but not available. Falling back to CPU.")
            return "cpu"
        if preferred == "cuda" and not torch.cuda.is_available():
            print("WARNING: CUDA requested but not available. Falling back to CPU.")
            return "cpu"
        return preferred

    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def print_device_info(device: str) -> None:
    """Print information about the selected device."""
    print(f"Device:              {device}", end="")

    if device == "cuda":
        print(f" ({torch.cuda.get_device_name(0)})")
    elif device == "mps":
        print(" (Apple Silicon MPS)")
    else:
        print(" (CPU - slower training)")


def get_env_var(name: str, default: str | None = None) -> str | None:
    """Get environment variable with optional default."""
    return os.environ.get(name, default)


def load_agent_from_path(agent_path: Path) -> tuple[Any, str]:
    """Load agent from Python file path.

    Mirrors the cloud platform's agent loading mechanism.
    """
    if not agent_path.exists():
        raise FileNotFoundError(f"Agent file not found: {agent_path}")

    # Add agent directory to path for relative imports
    agent_dir = agent_path.parent.resolve()
    if str(agent_dir) not in sys.path:
        sys.path.insert(0, str(agent_dir))

    # Load the module
    spec = importlib.util.spec_from_file_location("agent_module", agent_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {agent_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_module"] = module
    spec.loader.exec_module(module)

    # Find the agent in the module
    agent = None
    agent_name = "unknown"

    # Check for registered agent via runtime registry
    try:
        from konic.runtime.agent import get_registered_agent

        registered_agent, _ = get_registered_agent()
        if registered_agent is not None:
            agent = registered_agent
            agent_name = getattr(registered_agent, "_konic_meta", {}).get("name", "unknown")
    except ImportError:
        pass

    # Fallback: look for 'agent' variable in module
    if agent is None and hasattr(module, "agent"):
        agent = module.agent
        agent_name = getattr(module, "AGENT_NAME", agent_path.stem)

    # Fallback: look for create_agent function
    if agent is None and hasattr(module, "create_agent"):
        agent = module.create_agent()
        agent_name = getattr(module, "AGENT_NAME", agent_path.stem)

    if agent is None:
        raise ValueError(
            f"No agent found in {agent_path}. "
            "Expected: 'agent' variable, 'create_agent()' function, or register_agent() call."
        )

    return agent, agent_name


def is_finetuning_agent(agent: Any) -> bool:
    """Check if agent is a finetuning agent (mirrors cloud platform logic)."""
    return hasattr(agent, "get_finetuning_method") and callable(
        getattr(agent, "get_finetuning_method")
    )


def setup_mlflow(config: TrainingConfig, agent_name: str) -> str | None:
    """Setup MLflow tracking if enabled."""
    if not config.use_mlflow:
        return None

    try:
        import mlflow  # type: ignore[import-not-found]

        mlflow.set_tracking_uri(config.mlflow_tracking_uri)

        experiment_name = f"konic-local-{agent_name}"
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            mlflow.create_experiment(experiment_name)
        mlflow.set_experiment(experiment_name)

        run = mlflow.start_run()
        return run.info.run_id

    except ImportError:
        print("WARNING: MLflow not installed. Install with: pip install mlflow")
        return None


def log_params_mlflow(agent: KonicFinetuningAgent) -> None:
    """Log agent parameters to MLflow."""
    try:
        import mlflow  # type: ignore[import-not-found]

        mlflow.log_param("training_type", "finetuning")
        mlflow.log_param("finetuning_method", str(agent.get_finetuning_method()))
        mlflow.log_param("base_model", agent.get_base_model())

        lora_config = agent.get_lora_config()
        if lora_config:
            mlflow.log_param("lora_r", lora_config.r)
            mlflow.log_param("lora_alpha", lora_config.lora_alpha)
            mlflow.log_param("use_lora", True)
        else:
            mlflow.log_param("use_lora", False)

        training_config = agent.get_training_config()
        if training_config:
            mlflow.log_param("learning_rate", training_config.learning_rate)
            mlflow.log_param("batch_size", training_config.batch_size)
            mlflow.log_param("kl_penalty_weight", training_config.kl_penalty_weight)

    except ImportError:
        pass


def log_metrics_mlflow(metrics: dict[str, float], step: int) -> None:
    """Log iteration metrics to MLflow."""
    try:
        import mlflow  # type: ignore[import-not-found]

        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
    except ImportError:
        pass


# =============================================================================
# Verbose Training Callback
# =============================================================================


def create_verbose_callback() -> Any:
    """Create a verbose callback for detailed training logs."""
    from konic.finetuning import KonicFinetuningCallback

    class VerboseCloudCallback(KonicFinetuningCallback):
        """Verbose callback mirroring cloud platform logging."""

        def __init__(self):
            super().__init__(
                log_interval=1,
                log_samples=True,
                max_samples_to_log=2,
                use_mlflow=False,
                verbose=True,
            )
            self._iter_start = 0.0
            self._full_prompts: list[str] = []
            self._full_responses: list[str] = []

        def on_iteration_begin(self, iteration: int) -> None:
            self._iter_start = time.time()
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
            self._full_prompts = prompts[:2]
            self._full_responses = responses[:2]

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

            if reward_breakdown:
                for name, values in reward_breakdown.items():
                    avg_val = statistics.mean(values)
                    print(f"             └─ {name}: {avg_val:.4f}")

            # Log generated samples with their individual rewards
            if self._full_prompts:
                print(f"\n  {'─' * 56}")
                print("  Generated Samples:")
                print(f"  {'─' * 56}")
                for i, (prompt, response) in enumerate(
                    zip(self._full_prompts, self._full_responses)
                ):
                    sample_reward = rewards[i] if i < len(rewards) else 0.0
                    prompt_display = prompt[:80] + "..." if len(prompt) > 80 else prompt
                    print(f"  [Sample {i + 1}] Reward: {sample_reward:.4f}")
                    print(f'    Prompt:   "{prompt_display}"')
                    print(f'    Response: "{response}"')
                    if reward_breakdown:
                        breakdown_str = " | ".join(
                            f"{k}: {v[i]:.3f}" for k, v in reward_breakdown.items() if i < len(v)
                        )
                        print(f"    Breakdown: {breakdown_str}")
                    print()
                print(f"  {'─' * 56}")

        def on_iteration_end(self, result: FinetuningIterationResult) -> None:
            elapsed = time.time() - self._iter_start
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

    return VerboseCloudCallback()


def run_finetuning(
    agent: KonicFinetuningAgent,
    config: TrainingConfig,
    agent_name: str,
    device: str,
) -> dict[str, Any]:
    """Run finetuning training (mirrors cloud platform's run_finetuning)."""
    from konic.finetuning import KonicFinetuningEngine

    print(f"[INFO] Running finetuning for agent: {agent_name}")
    print(f"[INFO] Base model: {agent.get_base_model()}")
    print(f"[INFO] Finetuning method: {agent.get_finetuning_method()}")
    print(f"[INFO] Device: {device}")

    lora_config = agent.get_lora_config()
    if lora_config:
        print(f"[INFO] LoRA config: r={lora_config.r}, alpha={lora_config.lora_alpha}")
    print()

    # Create checkpoint directory
    config.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # Initialize engine from agent
    engine = KonicFinetuningEngine.from_agent(agent)
    engine.checkpoint_dir = str(config.checkpoint_dir)
    engine.device = device

    # Attach verbose callback if verbose mode
    if config.verbose:
        engine.callback = create_verbose_callback()

    # Log parameters to MLflow if enabled
    if config.use_mlflow:
        log_params_mlflow(agent)

    # Calculate save_every
    save_every = config.checkpoint_interval if config.checkpoint_interval > 0 else None

    # Run training
    start_time = time.time()

    result = engine.train(
        max_iterations=config.iterations,
        save_every=save_every,
    )

    total_time = time.time() - start_time

    # Log final metrics
    final_metrics = {
        "final/reward_mean": result.final_reward_mean,
        "final/best_reward": result.best_reward,
        "final/best_iteration": result.best_iteration,
        "final/kl_divergence": result.final_kl_divergence,
        "final/total_time_sec": total_time,
    }

    if config.use_mlflow:
        try:
            import mlflow  # type: ignore[import-not-found]

            for key, value in final_metrics.items():
                mlflow.log_metric(key, value)
            mlflow.log_param("completed", True)
        except ImportError:
            pass

    return {
        "result": result,
        "total_time": total_time,
        "final_metrics": final_metrics,
    }


def run_traditional_rl(agent: Any, config: TrainingConfig, agent_name: str) -> dict[str, Any]:
    """Run traditional RL training (placeholder for completeness)."""
    print(f"[INFO] Traditional RL training for agent: {agent_name}")
    print("[WARNING] Traditional RL local training not yet implemented.")
    print("[INFO] Use RLlib/Ray directly for traditional RL training.")
    return {"error": "Traditional RL training not implemented in local runner"}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Local Finetuning Training - Mirrors Konic Cloud Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_training.py --agent-path ./agent.py
    python run_training.py --agent-path ./agent.py --iterations 50
    python run_training.py --agent-path ./agent.py --use-mlflow
        """,
    )

    # Get defaults from environment variables (cloud-style)
    default_agent_path = get_env_var("AGENT_PATH")
    default_iterations = int(get_env_var("ITERATIONS") or "100")
    default_checkpoint_interval = int(get_env_var("CHECKPOINT_INTERVAL") or "0")
    default_checkpoint_dir = get_env_var("CHECKPOINT_DIR") or "./checkpoints"
    default_use_mlflow = (get_env_var("USE_MLFLOW") or "false").lower() == "true"
    default_mlflow_uri = get_env_var("MLFLOW_TRACKING_URI") or "./mlruns"

    parser.add_argument(
        "--agent-path",
        type=Path,
        default=default_agent_path,
        help="Path to agent.py file (or set AGENT_PATH env var)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=default_iterations,
        help=f"Number of training iterations (default: {default_iterations})",
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=default_checkpoint_interval,
        help="Save checkpoint every N iterations, 0=final only (default: 0)",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=Path(default_checkpoint_dir),
        help="Directory to save checkpoints",
    )
    parser.add_argument(
        "--use-mlflow",
        action="store_true",
        default=default_use_mlflow,
        help="Enable MLflow metrics logging",
    )
    parser.add_argument(
        "--mlflow-uri",
        type=str,
        default=default_mlflow_uri,
        help="MLflow tracking URI",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=get_env_var("DEVICE"),
        help="Device to use (cpu, cuda, mps). Auto-detected if not set.",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for local training."""
    args = parse_args()

    # Validate agent path
    if args.agent_path is None:
        print("ERROR: Agent path is required.")
        print("Usage: python run_training.py --agent-path /path/to/agent.py")
        print("   Or: AGENT_PATH=/path/to/agent.py python run_training.py")
        return 1

    # Detect best device
    device = get_best_device(args.device)

    # Create config
    config = TrainingConfig(
        agent_path=Path(args.agent_path),
        iterations=args.iterations,
        checkpoint_interval=args.checkpoint_interval,
        checkpoint_dir=args.checkpoint_dir,
        use_mlflow=args.use_mlflow,
        mlflow_tracking_uri=args.mlflow_uri,
        verbose=not args.quiet,
        device=device,
    )

    # Print banner
    print("=" * 70)
    print("Konic Local Training - Cloud Platform Mirror")
    print("=" * 70)
    print(f"Agent Path:          {config.agent_path}")
    print(f"Iterations:          {config.iterations}")
    print(f"Checkpoint Interval: {config.checkpoint_interval or 'final only'}")
    print(f"Checkpoint Dir:      {config.checkpoint_dir}")
    print(f"MLflow Enabled:      {config.use_mlflow}")
    print_device_info(device)
    print("=" * 70)
    print()

    try:
        # Load agent
        print("[STEP 1/4] Loading agent from file...")
        agent, agent_name = load_agent_from_path(config.agent_path)
        print(f"[OK] Agent loaded: {agent_name}")
        print()

        # Detect agent type
        print("[STEP 2/4] Detecting agent type...")
        if is_finetuning_agent(agent):
            print("[OK] Detected: Finetuning Agent (RLHF)")
            training_type = "finetuning"
        else:
            print("[OK] Detected: Traditional RL Agent")
            training_type = "rl"
        print()

        # Setup MLflow if enabled
        run_id = None
        if config.use_mlflow:
            print("[STEP 3/4] Setting up MLflow tracking...")
            run_id = setup_mlflow(config, agent_name)
            if run_id:
                print(f"[OK] MLflow run ID: {run_id}")
            else:
                print("[WARNING] MLflow setup failed, continuing without tracking")
        else:
            print("[STEP 3/4] Skipping MLflow (not enabled)")
        print()

        # Run training
        print("[STEP 4/4] Starting training...")
        print("-" * 70)

        if training_type == "finetuning":
            result = run_finetuning(agent, config, agent_name, device)
        else:
            result = run_traditional_rl(agent, config, agent_name)

        print("-" * 70)
        print()

        # Print results
        print("=" * 70)
        print("Training Complete!")
        print("=" * 70)

        if "result" in result:
            training_result = result["result"]
            print(training_result.summary())
            print()
            print(f"Total Time: {result['total_time']:.1f} seconds")
            print(f"Model Path: {training_result.model_path}")
        else:
            print(f"Result: {result}")

        # End MLflow run
        if config.use_mlflow and run_id:
            try:
                import mlflow  # type: ignore[import-not-found]

                mlflow.end_run()
                print(f"\n[INFO] MLflow run completed: {run_id}")
            except ImportError:
                pass

        print()
        print("=" * 70)

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1

    except ImportError as e:
        print(f"ERROR: Missing dependency - {e}")
        print("Install with: pip install konic[finetuning]")
        return 1

    except Exception as e:
        print(f"ERROR: Training failed - {e}")

        # Log failure to MLflow if enabled
        if config.use_mlflow:
            try:
                import mlflow  # type: ignore[import-not-found]

                mlflow.log_param("completed", False)
                mlflow.set_tag("error_message", str(e)[:500])
                mlflow.end_run(status="FAILED")
            except ImportError:
                pass

        raise


if __name__ == "__main__":
    sys.exit(main())

import traceback
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import Any

import ray
from ray.rllib.algorithms.algorithm import Algorithm
from ray.rllib.callbacks.callbacks import RLlibCallback
from ray.rllib.core.rl_module import RLModuleSpec
from ray.tune.registry import register_env

from konic.agent import KonicAgent
from konic.callback import KonicRLCallback
from konic.engine.utils import get_module_factory


@dataclass
class TrainingResult:
    """Result from a single training iteration with metrics for external logging."""

    iteration: int
    episode_return_mean: float = 0.0
    episode_length_mean: float = 0.0
    num_episodes: int = 0
    num_env_steps: int = 0
    num_env_steps_lifetime: int = 0
    num_episodes_lifetime: int = 0
    time_total_s: float = 0.0
    fps: float = 0.0
    learner_metrics: dict[str, dict[str, float]] = field(default_factory=dict)
    raw_result: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_rllib_result(cls, result: dict[str, Any], iteration: int) -> "TrainingResult":
        """Create TrainingResult from RLlib Algorithm.train() result dict."""
        env_runners = result.get("env_runners", {})

        learner_metrics = {}
        for learner_id, learner_data in result.get("learners", {}).items():
            learner_metrics[learner_id] = {
                "policy_loss": learner_data.get("policy_loss", 0.0),
                "value_loss": learner_data.get("vf_loss", 0.0),
                "entropy": learner_data.get("entropy", 0.0),
                "kl_divergence": learner_data.get("kl", 0.0),
                "learning_rate": learner_data.get("curr_lr", 0.0),
                "grad_norm": learner_data.get("grad_gnorm", 0.0),
                "total_loss": learner_data.get("total_loss", 0.0),
            }

        time_total = result.get("time_total_s", 1.0)
        steps_lifetime = result.get("num_env_steps_sampled_lifetime", 0)
        fps = steps_lifetime / max(time_total, 0.001)

        return cls(
            iteration=iteration,
            episode_return_mean=env_runners.get("episode_return_mean", 0.0),
            episode_length_mean=env_runners.get("episode_len_mean", 0.0),
            num_episodes=result.get("num_episodes", 0),
            num_env_steps=result.get("num_env_steps_sampled", 0),
            num_env_steps_lifetime=steps_lifetime,
            num_episodes_lifetime=result.get("num_episodes_lifetime", 0),
            time_total_s=time_total,
            fps=fps,
            learner_metrics=learner_metrics,
            raw_result=result,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to flat dict for WandB/TensorBoard logging."""
        metrics = {
            "iteration": self.iteration,
            "episode_return_mean": self.episode_return_mean,
            "episode_length_mean": self.episode_length_mean,
            "num_episodes": self.num_episodes,
            "num_env_steps": self.num_env_steps,
            "num_env_steps_lifetime": self.num_env_steps_lifetime,
            "num_episodes_lifetime": self.num_episodes_lifetime,
            "time_total_s": self.time_total_s,
            "fps": self.fps,
        }

        for learner_id, learner_data in self.learner_metrics.items():
            for key, value in learner_data.items():
                metrics[f"learner/{learner_id}/{key}"] = value

        return metrics


class KonicEngine:
    def __init__(
        self,
        agent: KonicAgent,
        callback: type[RLlibCallback] | None = None,
    ):
        self.agent = agent
        self.callback = callback if callback is not None else KonicRLCallback
        self._algo: Algorithm | None = None
        self._training_results: list[TrainingResult] = []

    @property
    def algorithm(self) -> Algorithm | None:
        return self._algo

    @property
    def training_results(self) -> list[TrainingResult]:
        return self._training_results.copy()

    @property
    def latest_result(self) -> TrainingResult | None:
        return self._training_results[-1] if self._training_results else None

    def _build_algorithm(self) -> Algorithm:
        module = self.agent.get_module()
        algorithm = module.algorithm
        environment = self.agent.get_environment()

        algo_config = get_module_factory(algorithm)

        def _register_environment(config):
            return environment

        register_env("konic-environment", _register_environment)

        if not ray.is_initialized():
            ray.init(include_dashboard=False)

        config = (
            algo_config()
            .framework("torch")
            .environment("konic-environment")
            .api_stack(enable_rl_module_and_learner=True, enable_env_runner_and_connector_v2=True)
            .rl_module(
                rl_module_spec=RLModuleSpec(module_class=module),
            )
            .callbacks(callbacks_class=self.callback)
            .env_runners(num_env_runners=2)
            .training(
                train_batch_size_per_learner=512,
                minibatch_size=64,
            )
        )

        return config.build_algo()

    def train(self, iterations: int) -> list[TrainingResult]:
        """Train for N iterations, blocking until complete."""
        results = list(self.train_iter(iterations))
        return results

    def train_iter(self, iterations: int) -> Generator[TrainingResult, None, None]:
        """Generator that yields TrainingResult after each iteration."""
        try:
            self._algo = self._build_algorithm()

            for i in range(iterations):
                raw_result = self._algo.train()
                result = TrainingResult.from_rllib_result(raw_result, iteration=i + 1)
                self._training_results.append(result)
                yield result

        except Exception:
            traceback.print_exc()
        finally:
            if ray.is_initialized():
                ray.shutdown()

    def stop(self) -> None:
        if self._algo is not None:
            self._algo.stop()
            self._algo = None
        if ray.is_initialized():
            ray.shutdown()

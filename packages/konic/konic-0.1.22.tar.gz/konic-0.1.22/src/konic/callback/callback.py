"""Customizable RL training callback for Konic metric tracking."""

from __future__ import annotations

import logging
from collections import deque
from typing import TYPE_CHECKING, Any, cast

from ray.rllib.callbacks.callbacks import RLlibCallback

from konic.callback.utils import get_custom_metric_fns

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ray.rllib.algorithms.algorithm import Algorithm
    from ray.rllib.env.env_runner import EnvRunner
    from ray.rllib.evaluation.episode_v2 import EpisodeV2
    from ray.rllib.utils.metrics.metrics_logger import MetricsLogger
    from ray.rllib.utils.typing import EpisodeType


class KonicRLCallback(RLlibCallback):
    """RL callback tracking episode/training metrics with extensible @custom_metric support."""

    def __init__(self, history_maxlen: int = 10000):
        super().__init__()
        self.total_episodes: int = 0
        self.total_steps: int = 0
        self._history_maxlen = history_maxlen
        self.episode_returns: deque[float] = deque(maxlen=history_maxlen)
        self.episode_lengths: deque[int] = deque(maxlen=history_maxlen)

    def on_episode_created(
        self,
        *,
        episode: EpisodeType | EpisodeV2,
        env_runner: EnvRunner | None = None,
        metrics_logger: MetricsLogger | None = None,
        env_index: int = 0,
        rl_module: Any = None,
        worker: Any = None,
        base_env: Any = None,
        policies: Any = None,
        **kwargs,
    ) -> None:
        if hasattr(episode, "custom_data"):
            ep = cast(Any, episode)
            ep.custom_data["konic_step_rewards"] = []
            ep.custom_data["konic_step_count"] = 0

    def on_episode_start(
        self,
        *,
        episode: EpisodeType | EpisodeV2,
        env_runner: EnvRunner | None = None,
        metrics_logger: MetricsLogger | None = None,
        env_index: int = 0,
        rl_module: Any = None,
        worker: Any = None,
        base_env: Any = None,
        policies: Any = None,
        **kwargs,
    ) -> None:
        pass

    def on_episode_step(
        self,
        *,
        episode: EpisodeType | EpisodeV2,
        env_runner: EnvRunner | None = None,
        metrics_logger: MetricsLogger | None = None,
        env_index: int = 0,
        rl_module: Any = None,
        worker: Any = None,
        base_env: Any = None,
        policies: Any = None,
        **kwargs,
    ) -> None:
        if hasattr(episode, "custom_data"):
            ep = cast(Any, episode)
            ep.custom_data["konic_step_count"] += 1

            if hasattr(episode, "get_rewards"):
                rewards = ep.get_rewards()
                if len(rewards) > 0:
                    ep.custom_data["konic_step_rewards"].append(rewards[-1])

    def on_episode_end(
        self,
        *,
        episode: EpisodeType | EpisodeV2,
        env_runner: EnvRunner | None = None,
        metrics_logger: MetricsLogger | None = None,
        env_index: int = 0,
        rl_module: Any = None,
        worker: Any = None,
        base_env: Any = None,
        policies: Any = None,
        **kwargs,
    ) -> None:
        episode_return: float = 0.0
        episode_length: int = 0
        ep = cast(Any, episode)

        if hasattr(episode, "get_return"):
            episode_return = ep.get_return()
        if hasattr(episode, "custom_data"):
            episode_length = ep.custom_data.get(
                "konic_step_count",
                len(ep.get_rewards()) if hasattr(episode, "get_rewards") else 0,
            )

        self.total_episodes += 1
        self.total_steps += episode_length
        self.episode_returns.append(episode_return)
        self.episode_lengths.append(episode_length)

        if metrics_logger is not None:
            metrics_logger.log_value(
                "konic/episode_return", episode_return, reduce="mean", window=100
            )
            metrics_logger.log_value(
                "konic/episode_length", episode_length, reduce="mean", window=100
            )
            metrics_logger.log_value("konic/total_episodes", self.total_episodes)
            metrics_logger.log_value("konic/total_steps", self.total_steps)

            self._process_custom_metrics(episode, metrics_logger)

    def on_train_result(
        self,
        *,
        algorithm: Algorithm,
        metrics_logger: MetricsLogger | None = None,
        result: dict[str, Any],
        **kwargs,
    ) -> None:
        if metrics_logger is not None:
            self._log_training_metrics(result, metrics_logger)

    def _process_custom_metrics(
        self,
        episode: EpisodeType | EpisodeV2,
        metrics_logger: MetricsLogger,
    ) -> None:
        custom_fns = get_custom_metric_fns(self)
        for fn in custom_fns:
            try:
                metrics = fn(episode)
                if isinstance(metrics, dict):
                    for key, value in metrics.items():
                        metrics_logger.log_value(
                            f"konic/custom/{key}",
                            value,
                            reduce="mean",
                            window=50,
                        )
            except Exception as e:
                logger.warning(f"Custom metric function {fn.__name__} failed: {e}")

    def _log_training_metrics(
        self,
        result: dict[str, Any],
        metrics_logger: MetricsLogger,
    ) -> None:
        self._log_episode_metrics(result, metrics_logger)

        learner_results = result.get("learners", {})
        for learner_id, learner_data in learner_results.items():
            self._log_learner_metrics(learner_id, learner_data, metrics_logger)

        self._log_throughput_metrics(result, metrics_logger)

    def _log_learner_metrics(
        self,
        learner_id: str,
        learner_data: dict[str, Any],
        metrics_logger: MetricsLogger,
    ) -> None:
        metric_mappings = {
            "policy_loss": "policy_loss",
            "vf_loss": "value_loss",
            "entropy": "entropy",
            "kl": "kl_divergence",
            "curr_lr": "learning_rate",
            "grad_gnorm": "grad_norm",
            "total_loss": "total_loss",
            "mean_kl_loss": "mean_kl_loss",
            "curr_entropy_coeff": "entropy_coeff",
            "vf_loss_unclipped": "vf_loss_unclipped",
            "vf_explained_var": "vf_explained_var",
            "curr_kl_coeff": "kl_coeff",
            "num_module_steps_trained": "steps_trained",
        }

        for source_key, target_key in metric_mappings.items():
            if source_key in learner_data:
                metrics_logger.log_value(
                    f"konic/learner/{learner_id}/{target_key}",
                    learner_data[source_key],
                )

    def _log_episode_metrics(
        self,
        result: dict[str, Any],
        metrics_logger: MetricsLogger,
    ) -> None:
        env_runners = result.get("env_runners", {})

        episode_metric_mappings = {
            "episode_return_mean": "return_mean",
            "episode_return_min": "return_min",
            "episode_return_max": "return_max",
            "episode_len_mean": "length_mean",
            "episode_len_min": "length_min",
            "episode_len_max": "length_max",
        }

        for source_key, target_key in episode_metric_mappings.items():
            if source_key in env_runners:
                metrics_logger.log_value(
                    f"konic/episode/{target_key}",
                    env_runners[source_key],
                )

    def _log_throughput_metrics(
        self,
        result: dict[str, Any],
        metrics_logger: MetricsLogger,
    ) -> None:
        if "time_total_s" in result and "num_env_steps_sampled_lifetime" in result:
            time_s = result["time_total_s"]
            # Only report FPS for runs with meaningful duration (>0.1s)
            if time_s > 0.1:
                fps = result["num_env_steps_sampled_lifetime"] / time_s
                metrics_logger.log_value("konic/throughput/fps", fps)

        if "num_env_steps_sampled_lifetime" in result:
            metrics_logger.log_value(
                "konic/throughput/total_env_steps",
                result["num_env_steps_sampled_lifetime"],
            )

        if "num_episodes_lifetime" in result:
            metrics_logger.log_value(
                "konic/throughput/total_episodes",
                result["num_episodes_lifetime"],
            )

        if "training_iteration" in result:
            metrics_logger.log_value(
                "konic/throughput/training_iteration",
                result["training_iteration"],
            )

        if "time_total_s" in result:
            metrics_logger.log_value(
                "konic/time/total_s",
                result["time_total_s"],
            )

        if "time_this_iter_s" in result:
            metrics_logger.log_value(
                "konic/time/this_iter_s",
                result["time_this_iter_s"],
            )

    def get_episode_returns(self) -> list[float]:
        return list(self.episode_returns)

    def get_episode_lengths(self) -> list[int]:
        return list(self.episode_lengths)

    def get_mean_return(self, window: int = 100) -> float:
        if not self.episode_returns:
            return 0.0
        # Use list conversion for slicing since deque doesn't support negative slicing
        recent = list(self.episode_returns)[-window:]
        return sum(recent) / len(recent)

    def get_mean_length(self, window: int = 100) -> float:
        if not self.episode_lengths:
            return 0.0
        recent = list(self.episode_lengths)[-window:]
        return sum(recent) / len(recent)

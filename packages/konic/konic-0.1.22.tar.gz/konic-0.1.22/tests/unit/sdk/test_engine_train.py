# pyright: reportArgumentType=false, reportOptionalMemberAccess=false
"""Tests for konic.engine.train module."""

from unittest.mock import MagicMock, patch

import pytest

from konic.engine.train import KonicEngine, TrainingResult


class TestTrainingResult:
    """Tests for TrainingResult dataclass."""

    def test_default_values(self):
        result = TrainingResult(iteration=1)

        assert result.iteration == 1
        assert result.episode_return_mean == 0.0
        assert result.episode_length_mean == 0.0
        assert result.num_episodes == 0
        assert result.num_env_steps == 0
        assert result.num_env_steps_lifetime == 0
        assert result.num_episodes_lifetime == 0
        assert result.time_total_s == 0.0
        assert result.fps == 0.0
        assert result.learner_metrics == {}
        assert result.raw_result == {}

    def test_custom_values(self):
        learner_data = {"learner_1": {"policy_loss": 0.5}}
        raw = {"custom": "data"}

        result = TrainingResult(
            iteration=5,
            episode_return_mean=100.5,
            episode_length_mean=50.2,
            num_episodes=10,
            num_env_steps=1000,
            num_env_steps_lifetime=5000,
            num_episodes_lifetime=50,
            time_total_s=120.0,
            fps=41.6,
            learner_metrics=learner_data,
            raw_result=raw,
        )

        assert result.iteration == 5
        assert result.episode_return_mean == 100.5
        assert result.episode_length_mean == 50.2
        assert result.num_episodes == 10
        assert result.num_env_steps == 1000
        assert result.num_env_steps_lifetime == 5000
        assert result.num_episodes_lifetime == 50
        assert result.time_total_s == 120.0
        assert result.fps == 41.6
        assert result.learner_metrics == learner_data
        assert result.raw_result == raw

    def test_from_rllib_result_basic(self):
        rllib_result = {
            "env_runners": {
                "episode_return_mean": 150.0,
                "episode_len_mean": 75.0,
            },
            "num_episodes": 20,
            "num_env_steps_sampled": 2000,
            "num_env_steps_sampled_lifetime": 10000,
            "num_episodes_lifetime": 100,
            "time_total_s": 60.0,
            "learners": {},
        }

        result = TrainingResult.from_rllib_result(rllib_result, iteration=3)

        assert result.iteration == 3
        assert result.episode_return_mean == 150.0
        assert result.episode_length_mean == 75.0
        assert result.num_episodes == 20
        assert result.num_env_steps == 2000
        assert result.num_env_steps_lifetime == 10000
        assert result.num_episodes_lifetime == 100
        assert result.time_total_s == 60.0
        assert result.fps == pytest.approx(10000 / 60.0)

    def test_from_rllib_result_with_learners(self):
        rllib_result = {
            "env_runners": {},
            "learners": {
                "default_policy": {
                    "policy_loss": 0.1,
                    "vf_loss": 0.2,
                    "entropy": 0.5,
                    "kl": 0.01,
                    "curr_lr": 0.001,
                    "grad_gnorm": 2.5,
                    "total_loss": 0.3,
                }
            },
            "time_total_s": 10.0,
            "num_env_steps_sampled_lifetime": 1000,
        }

        result = TrainingResult.from_rllib_result(rllib_result, iteration=1)

        assert "default_policy" in result.learner_metrics
        metrics = result.learner_metrics["default_policy"]
        assert metrics["policy_loss"] == 0.1
        assert metrics["value_loss"] == 0.2
        assert metrics["entropy"] == 0.5
        assert metrics["kl_divergence"] == 0.01
        assert metrics["learning_rate"] == 0.001
        assert metrics["grad_norm"] == 2.5
        assert metrics["total_loss"] == 0.3

    def test_from_rllib_result_empty(self):
        result = TrainingResult.from_rllib_result({}, iteration=1)

        assert result.iteration == 1
        assert result.episode_return_mean == 0.0
        assert result.learner_metrics == {}

    def test_from_rllib_result_zero_time(self):
        rllib_result = {
            "time_total_s": 0.0,
            "num_env_steps_sampled_lifetime": 1000,
        }

        result = TrainingResult.from_rllib_result(rllib_result, iteration=1)
        # Should handle division by zero gracefully
        assert result.fps == 1000 / 0.001  # Uses max(time_total, 0.001)

    def test_to_dict(self):
        result = TrainingResult(
            iteration=2,
            episode_return_mean=50.0,
            episode_length_mean=25.0,
            num_episodes=5,
            num_env_steps=500,
            num_env_steps_lifetime=2500,
            num_episodes_lifetime=25,
            time_total_s=30.0,
            fps=83.3,
            learner_metrics={"learner_0": {"policy_loss": 0.1, "value_loss": 0.2}},
        )

        metrics = result.to_dict()

        assert metrics["iteration"] == 2
        assert metrics["episode_return_mean"] == 50.0
        assert metrics["episode_length_mean"] == 25.0
        assert metrics["num_episodes"] == 5
        assert metrics["num_env_steps"] == 500
        assert metrics["num_env_steps_lifetime"] == 2500
        assert metrics["num_episodes_lifetime"] == 25
        assert metrics["time_total_s"] == 30.0
        assert metrics["fps"] == 83.3
        assert metrics["learner/learner_0/policy_loss"] == 0.1
        assert metrics["learner/learner_0/value_loss"] == 0.2

    def test_to_dict_no_learner_metrics(self):
        result = TrainingResult(iteration=1)
        metrics = result.to_dict()

        assert "learner" not in str(metrics.keys())


class TestKonicEngine:
    """Tests for KonicEngine class."""

    def test_init(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        assert engine.agent is mock_agent
        assert engine._algo is None
        assert engine._training_results == []

    def test_init_with_callback(self):
        mock_agent = MagicMock()
        mock_callback_cls = MagicMock()

        engine = KonicEngine(agent=mock_agent, callback=mock_callback_cls)

        assert engine.callback is mock_callback_cls

    def test_algorithm_property(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        assert engine.algorithm is None

        mock_algo = MagicMock()
        engine._algo = mock_algo
        assert engine.algorithm is mock_algo

    def test_training_results_property(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        assert engine.training_results == []

        result1 = TrainingResult(iteration=1)
        result2 = TrainingResult(iteration=2)
        engine._training_results = [result1, result2]

        results = engine.training_results
        assert len(results) == 2
        # Should return a copy
        results.append(TrainingResult(iteration=3))
        assert len(engine._training_results) == 2

    def test_latest_result_property_empty(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        assert engine.latest_result is None

    def test_latest_result_property(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        result1 = TrainingResult(iteration=1)
        result2 = TrainingResult(iteration=2, episode_return_mean=100.0)
        engine._training_results = [result1, result2]

        assert engine.latest_result is result2
        assert engine.latest_result.episode_return_mean == 100.0

    def test_stop(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        mock_algo = MagicMock()
        engine._algo = mock_algo

        with patch("konic.engine.train.ray") as mock_ray:
            mock_ray.is_initialized.return_value = True

            engine.stop()

            mock_algo.stop.assert_called_once()
            assert engine._algo is None
            mock_ray.shutdown.assert_called_once()

    def test_stop_no_algo(self):
        mock_agent = MagicMock()
        engine = KonicEngine(agent=mock_agent)

        with patch("konic.engine.train.ray") as mock_ray:
            mock_ray.is_initialized.return_value = False

            engine.stop()

            mock_ray.shutdown.assert_not_called()

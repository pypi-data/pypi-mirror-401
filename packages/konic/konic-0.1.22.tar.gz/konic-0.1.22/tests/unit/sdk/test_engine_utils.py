"""Tests for konic.engine.utils module."""

from konic.engine.utils import get_module_factory
from konic.module.type import KonicAlgorithmType


class TestGetModuleFactory:
    """Tests for get_module_factory function."""

    def test_returns_ppo_config_for_ppo(self):
        from ray.rllib.algorithms.ppo import PPOConfig

        result = get_module_factory(KonicAlgorithmType.PPO)

        assert result is PPOConfig

    def test_returns_algorithm_config_type(self):
        from ray.rllib.algorithms import AlgorithmConfig

        result = get_module_factory(KonicAlgorithmType.PPO)

        assert issubclass(result, AlgorithmConfig)

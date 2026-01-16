# pyright: reportAbstractUsage=false, reportAttributeAccessIssue=false
"""Tests for konic.environment.base module."""

from abc import ABC
from unittest.mock import MagicMock

import gymnasium as gym
import numpy as np
import pytest

from konic.environment.base import BaseKonicEnvironment


class TestBaseKonicEnvironment:
    """Tests for BaseKonicEnvironment abstract class."""

    def test_is_abstract_class(self):
        assert issubclass(BaseKonicEnvironment, ABC)

    def test_inherits_from_gym_env(self):
        assert issubclass(BaseKonicEnvironment, gym.Env)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError) as exc_info:
            BaseKonicEnvironment()
        assert "abstract" in str(exc_info.value).lower()

    def test_abstract_properties_exist(self):
        assert hasattr(BaseKonicEnvironment, "reward_composer")
        assert hasattr(BaseKonicEnvironment, "termination_composer")

    def test_abstract_methods_exist(self):
        assert hasattr(BaseKonicEnvironment, "step")
        assert hasattr(BaseKonicEnvironment, "reset")
        assert hasattr(BaseKonicEnvironment, "get_obs")
        assert hasattr(BaseKonicEnvironment, "get_info")

    def test_concrete_implementation(self):
        class ConcreteEnv(BaseKonicEnvironment):
            def __init__(self):
                super().__init__()
                self._state = np.zeros(4, dtype=np.float32)
                self._reward_composer = MagicMock()
                self._termination_composer = MagicMock()
                self.action_space = gym.spaces.Discrete(2)
                self.observation_space = gym.spaces.Box(
                    low=-1, high=1, shape=(4,), dtype=np.float32
                )

            @property
            def reward_composer(self):
                return self._reward_composer

            @property
            def termination_composer(self):
                return self._termination_composer

            def step(self, action):
                reward = self._reward_composer.compose()
                terminated = self._termination_composer.compose()
                return self._state.copy(), reward, terminated, False, {}

            def reset(self, *, seed=None, options=None):
                self._state = np.zeros(4, dtype=np.float32)
                return self._state.copy(), {}

            def get_obs(self):
                return self._state.copy()

            def get_info(self):
                return {"custom": "info"}

        env = ConcreteEnv()

        # Test init
        assert env.action_space.n == 2
        assert env.observation_space.shape == (4,)

        # Test reset
        obs, info = env.reset()
        assert obs.shape == (4,)
        assert info == {}

        # Test step
        env._reward_composer.compose.return_value = 1.0
        env._termination_composer.compose.return_value = False
        obs, reward, term, trunc, info = env.step(0)
        assert reward == 1.0
        assert term is False

        # Test get_obs
        obs = env.get_obs()
        assert obs.shape == (4,)

        # Test get_info
        assert env.get_info() == {"custom": "info"}

    def test_partial_implementation_fails(self):
        class PartialEnv(BaseKonicEnvironment):
            def __init__(self):
                super().__init__()

            @property
            def reward_composer(self):
                return MagicMock()

            # Missing other methods

        with pytest.raises(TypeError):
            PartialEnv()

# pyright: reportArgumentType=false
"""Tests for konic.environment.core module."""

from unittest.mock import MagicMock

import gymnasium as gym
import numpy as np
import pytest

from konic.environment.core import KonicEnvironment
from konic.environment.reward import KonicRewardComposer
from konic.environment.space import KonicSpace
from konic.environment.termination import KonicTerminationComposer


class TestKonicEnvironment:
    """Tests for KonicEnvironment class."""

    def create_mock_spaces(self):
        """Create mock action and observation spaces."""
        action_space = MagicMock(spec=KonicSpace)
        action_space.to_gym.return_value = gym.spaces.Discrete(4)

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(4,), dtype=np.float32
        )

        return action_space, obs_space

    def test_init(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        assert env._konic_action_space is action_space
        assert env._konic_observation_space is obs_space
        reward_composer.set_env.assert_called_once_with(env)
        term_composer.set_env.assert_called_once_with(env)

    def test_action_space_property(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        assert isinstance(env.action_space, gym.spaces.Discrete)
        assert env.action_space.n == 4

    def test_observation_space_property(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        assert isinstance(env.observation_space, gym.spaces.Box)
        assert env.observation_space.shape == (4,)

    def test_reward_composer_property(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        assert env.reward_composer is reward_composer

    def test_termination_composer_property(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        assert env.termination_composer is term_composer

    def test_step_not_implemented(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        with pytest.raises(NotImplementedError) as exc_info:
            env.step({"action": 0})
        assert "_step() is not implemented" in str(exc_info.value)

    def test_reset_not_implemented(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        with pytest.raises(NotImplementedError) as exc_info:
            env.reset()
        assert "_reset() is not implemented" in str(exc_info.value)

    def test_get_obs_not_implemented(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        with pytest.raises(NotImplementedError) as exc_info:
            env.get_obs()
        assert "get_obs() is not implemented" in str(exc_info.value)

    def test_get_info_default(self):
        action_space, obs_space = self.create_mock_spaces()
        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        assert env.get_info() == {}


class TestKonicEnvironmentFlattenSpaces:
    """Tests for KonicEnvironment with flatten_spaces=True."""

    def test_flatten_dict_obs_space(self):
        action_space = MagicMock(spec=KonicSpace)
        action_space.to_gym.return_value = gym.spaces.Discrete(2)

        obs_space = MagicMock(spec=KonicSpace)
        dict_obs = gym.spaces.Dict(
            {
                "position": gym.spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32),
                "velocity": gym.spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32),
            }
        )
        obs_space.to_gym.return_value = dict_obs

        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
            flatten_spaces=True,
        )

        # Observation space should be flattened
        assert isinstance(env.observation_space, gym.spaces.Box)
        assert env.observation_space.shape == (6,)  # 3 + 3

    def test_flatten_dict_action_space(self):
        action_space = MagicMock(spec=KonicSpace)
        dict_action = gym.spaces.Dict(
            {
                "main_action": gym.spaces.Discrete(4),
            }
        )
        action_space.to_gym.return_value = dict_action

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
            flatten_spaces=True,
        )

        # Action space should be the Discrete from the dict
        assert isinstance(env.action_space, gym.spaces.Discrete)
        assert env.action_space.n == 4

    def test_flatten_dict_obs_method(self):
        action_space = MagicMock(spec=KonicSpace)
        action_space.to_gym.return_value = gym.spaces.Discrete(2)

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        # Test flattening dict observation
        obs_dict = {
            "a": np.array([1.0, 2.0]),
            "b": np.array([3.0]),
        }

        flattened = env._flatten_dict_obs(obs_dict)

        assert isinstance(flattened, np.ndarray)
        assert flattened.dtype == np.float32
        assert len(flattened) == 3  # 2 + 1

    def test_flatten_dict_obs_non_dict(self):
        action_space = MagicMock(spec=KonicSpace)
        action_space.to_gym.return_value = gym.spaces.Discrete(2)

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        # Non-dict should be returned as-is
        obs_array = np.array([1.0, 2.0, 3.0])
        result = env._flatten_dict_obs(obs_array)
        np.testing.assert_array_equal(result, obs_array)

    def test_extract_dict_action_already_dict(self):
        action_space = MagicMock(spec=KonicSpace)
        action_space.to_gym.return_value = gym.spaces.Discrete(2)

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        action_dict = {"action": 1}
        result = env._extract_dict_action(action_dict)
        assert result == action_dict

    def test_extract_dict_action_from_discrete(self):
        action_space = MagicMock(spec=KonicSpace)
        dict_action_space = gym.spaces.Dict({"main": gym.spaces.Discrete(4)})
        action_space.to_gym.return_value = dict_action_space

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        reward_composer = MagicMock(spec=KonicRewardComposer)
        term_composer = MagicMock(spec=KonicTerminationComposer)

        env = KonicEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
            flatten_spaces=True,
        )

        # Scalar action should be wrapped in dict
        result = env._extract_dict_action(2)
        assert result == {"main": 2}


class TestConcreteKonicEnvironment:
    """Tests for a concrete KonicEnvironment implementation."""

    def test_concrete_implementation(self):
        class MyEnvironment(KonicEnvironment):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._state = np.zeros(4, dtype=np.float32)

            def _step(self, action):
                self._state += 0.1
                reward = self.reward_composer.compose()
                terminated = self.termination_composer.compose()
                return self._state.copy(), reward, terminated, False, {}

            def _reset(self, seed=None, options=None):
                self._state = np.zeros(4, dtype=np.float32)
                return self._state.copy(), {}

            def get_obs(self):
                return self._state.copy()

        action_space = MagicMock(spec=KonicSpace)
        action_space.to_gym.return_value = gym.spaces.Discrete(2)

        obs_space = MagicMock(spec=KonicSpace)
        obs_space.to_gym.return_value = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

        reward_composer = MagicMock(spec=KonicRewardComposer)
        reward_composer.compose.return_value = 1.0
        term_composer = MagicMock(spec=KonicTerminationComposer)
        term_composer.compose.return_value = False

        env = MyEnvironment(
            action_space=action_space,
            observation_space=obs_space,
            reward_composer=reward_composer,
            termination_composer=term_composer,
        )

        # Test reset
        obs, info = env.reset()
        assert obs.shape == (4,)
        np.testing.assert_array_equal(obs, np.zeros(4))
        assert info == {}

        # Test step
        obs, reward, terminated, truncated, info = env.step({"action": 1})
        assert obs.shape == (4,)
        assert reward == 1.0
        assert terminated is False
        assert truncated is False

        # Test get_obs
        obs = env.get_obs()
        assert obs.shape == (4,)

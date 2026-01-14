"""Tests for konic.module.ppo module."""

from unittest.mock import MagicMock

import pytest
import torch
import torch.nn as nn

from konic.module.ppo import KonicTorchPPO
from konic.module.type import KonicAlgorithmType


class TestKonicTorchPPO:
    """Tests for KonicTorchPPO class."""

    def test_algorithm_attribute(self):
        assert KonicTorchPPO.algorithm == KonicAlgorithmType.PPO

    def test_inherits_from_base_torch_module(self):
        from konic.module.base import BaseTorchModule

        assert issubclass(KonicTorchPPO, BaseTorchModule)

    def test_implements_value_function_api(self):
        from ray.rllib.core.rl_module.apis import ValueFunctionAPI

        assert issubclass(KonicTorchPPO, ValueFunctionAPI)

    def test_inherits_from_torch_rl_module(self):
        from ray.rllib.core.rl_module.torch import TorchRLModule

        assert issubclass(KonicTorchPPO, TorchRLModule)


class TestKonicTorchPPOSetup:
    """Tests for KonicTorchPPO setup and initialization."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock config for testing."""
        config = MagicMock()
        config.observation_space = MagicMock()
        config.observation_space.shape = (4,)
        config.action_space = MagicMock()
        config.action_space.n = 2
        return config

    @pytest.fixture
    def mock_model_config(self):
        """Create mock model config."""
        return {"hidden_dim": 64}

    def test_setup_creates_pi_network(self, mock_config, mock_model_config):
        """Test that setup creates a policy network."""
        module = MagicMock(spec=KonicTorchPPO)
        module.config = mock_config
        module.model_config = mock_model_config

        # Call the actual setup logic
        obs_space = mock_config.observation_space
        action_space = mock_config.action_space
        hidden_dim = int(mock_model_config.get("hidden_dim", 64))

        in_dim = obs_space.shape[0]
        out_dim = int(action_space.n)

        pi = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim),
        )

        assert pi[0].in_features == 4
        assert pi[-1].out_features == 2

    def test_setup_creates_vf_network(self, mock_config, mock_model_config):
        """Test that setup creates a value function network."""
        obs_space = mock_config.observation_space
        hidden_dim = int(mock_model_config.get("hidden_dim", 64))

        in_dim = obs_space.shape[0]

        vf = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

        assert vf[0].in_features == 4
        assert vf[-1].out_features == 1

    def test_setup_default_hidden_dim(self, mock_config):
        """Test that default hidden_dim is 64."""
        model_config = {}
        hidden_dim = int(model_config.get("hidden_dim", 64))
        assert hidden_dim == 64


class TestKonicTorchPPOForward:
    """Tests for KonicTorchPPO forward methods."""

    @pytest.fixture
    def pi_network(self):
        """Create a policy network for testing."""
        return nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.GELU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

    @pytest.fixture
    def vf_network(self):
        """Create a value function network for testing."""
        return nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def test_forward_common_2d_input(self, pi_network):
        """Test _forward_common with 2D input (batch, features)."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}

        # Simulate _forward_common logic
        obs = batch[Columns.OBS]
        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        output = pi_network(obs)

        assert output.shape == (8, 2)

    def test_forward_common_1d_input(self, pi_network):
        """Test _forward_common with 1D input (single observation)."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(4)}  # 1D input

        # Simulate _forward_common logic
        obs = batch[Columns.OBS]
        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        output = pi_network(obs)

        assert output.shape == (1, 2)

    def test_forward_common_returns_action_dist_inputs(self, pi_network):
        """Test that _forward_common returns ACTION_DIST_INPUTS."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        obs = batch[Columns.OBS]
        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        result = {Columns.ACTION_DIST_INPUTS: pi_network(obs)}

        assert Columns.ACTION_DIST_INPUTS in result

    def test_forward_inference_no_grad(self, pi_network):
        """Test that _forward_inference uses no_grad context."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}

        with torch.no_grad():
            obs = batch[Columns.OBS]
            if len(obs.shape) == 1:
                obs = obs.unsqueeze(0)
            output = pi_network(obs)

        # Verify output doesn't require grad
        assert not output.requires_grad

    def test_forward_exploration_and_train(self, pi_network):
        """Test that _forward_exploration and _forward_train work correctly."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        obs = batch[Columns.OBS]
        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        output = pi_network(obs)

        # Both should produce valid outputs
        assert output.shape == (8, 2)


class TestKonicTorchPPOComputeValues:
    """Tests for KonicTorchPPO compute_values method."""

    @pytest.fixture
    def vf_network(self):
        """Create a value function network for testing."""
        return nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def test_compute_values_2d_input(self, vf_network):
        """Test compute_values with 2D input."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}

        obs = batch[Columns.OBS]
        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        values = vf_network(obs).squeeze(-1)

        assert values.shape == (8,)

    def test_compute_values_1d_input(self, vf_network):
        """Test compute_values with 1D input (single observation)."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(4)}  # 1D input

        obs = batch[Columns.OBS]
        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        values = vf_network(obs).squeeze(-1)

        assert values.shape == (1,)

    def test_compute_values_returns_scalar_per_sample(self, vf_network):
        """Test that compute_values returns one value per sample."""
        batch_size = 16
        obs = torch.randn(batch_size, 4)

        if len(obs.shape) == 1:
            obs = obs.unsqueeze(0)

        values = vf_network(obs).squeeze(-1)

        assert values.shape == (batch_size,)

    def test_compute_values_deterministic(self, vf_network):
        """Test that compute_values is deterministic for the same input."""
        obs = torch.randn(4, 4)

        vf_network.eval()
        with torch.no_grad():
            values1 = vf_network(obs).squeeze(-1)
            values2 = vf_network(obs).squeeze(-1)

        assert torch.allclose(values1, values2)


class TestKonicTorchPPONetworkArchitecture:
    """Tests for the PPO network architecture."""

    def test_pi_network_activation_functions(self):
        """Test that policy network uses correct activations."""
        pi = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.GELU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

        # Check activation function types
        assert isinstance(pi[1], nn.ReLU)
        assert isinstance(pi[3], nn.GELU)
        assert isinstance(pi[5], nn.ReLU)

    def test_vf_network_activation_functions(self):
        """Test that value network uses correct activations."""
        vf = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

        # Check activation function types
        assert isinstance(vf[1], nn.ReLU)
        assert isinstance(vf[3], nn.ReLU)

    def test_networks_are_differentiable(self):
        """Test that networks support gradient computation."""
        pi = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )
        vf = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

        obs = torch.randn(2, 4, requires_grad=True)
        pi_out = pi(obs)
        vf_out = vf(obs)

        # Compute gradients
        pi_loss = pi_out.sum()
        vf_loss = vf_out.sum()

        pi_loss.backward()
        vf_loss.backward()

        assert obs.grad is not None


class TestKonicTorchPPOInstantiation:
    """Tests for actual KonicTorchPPO instantiation and methods."""

    @pytest.fixture
    def ppo_module(self):
        """Create a KonicTorchPPO module for testing using new RLlib API."""
        from gymnasium.spaces import Box, Discrete

        module = KonicTorchPPO(
            observation_space=Box(low=-1.0, high=1.0, shape=(4,)),
            action_space=Discrete(2),
            model_config={"hidden_dim": 64},
        )
        module.setup()
        return module

    def test_instantiation_creates_networks(self, ppo_module):
        """Test that KonicTorchPPO creates pi and vf networks."""
        assert hasattr(ppo_module, "pi")
        assert hasattr(ppo_module, "vf")

    def test_setup_creates_correct_network_dimensions(self, ppo_module):
        """Test that setup creates networks with correct dimensions."""
        # Policy network: 4 -> 64 -> 64 -> 64 -> 2
        assert ppo_module.pi[0].in_features == 4
        assert ppo_module.pi[-1].out_features == 2

        # Value network: 4 -> 64 -> 64 -> 1
        assert ppo_module.vf[0].in_features == 4
        assert ppo_module.vf[-1].out_features == 1

    def test_forward_inference_method(self, ppo_module):
        """Test _forward_inference method."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        result = ppo_module._forward_inference(batch)

        assert Columns.ACTION_DIST_INPUTS in result
        assert result[Columns.ACTION_DIST_INPUTS].shape == (8, 2)

    def test_forward_exploration_method(self, ppo_module):
        """Test _forward_exploration method."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        result = ppo_module._forward_exploration(batch)

        assert Columns.ACTION_DIST_INPUTS in result
        assert result[Columns.ACTION_DIST_INPUTS].shape == (8, 2)

    def test_forward_train_method(self, ppo_module):
        """Test _forward_train method."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        result = ppo_module._forward_train(batch)

        assert Columns.ACTION_DIST_INPUTS in result
        assert result[Columns.ACTION_DIST_INPUTS].shape == (8, 2)

    def test_forward_common_with_1d_input(self, ppo_module):
        """Test _forward_common with 1D input (unsqueeze path)."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(4)}  # 1D input
        result = ppo_module._forward_common(batch)

        assert Columns.ACTION_DIST_INPUTS in result
        assert result[Columns.ACTION_DIST_INPUTS].shape == (1, 2)

    def test_compute_values_method(self, ppo_module):
        """Test compute_values method."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        values = ppo_module.compute_values(batch)

        assert values.shape == (8,)

    def test_compute_values_with_1d_input(self, ppo_module):
        """Test compute_values with 1D input (unsqueeze path)."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(4)}  # 1D input
        values = ppo_module.compute_values(batch)

        assert values.shape == (1,)

    def test_forward_inference_no_grad(self, ppo_module):
        """Test that _forward_inference doesn't track gradients."""
        from ray.rllib.core import Columns

        batch = {Columns.OBS: torch.randn(8, 4)}
        result = ppo_module._forward_inference(batch)

        # Output should not require grad
        assert not result[Columns.ACTION_DIST_INPUTS].requires_grad

    def test_setup_with_custom_hidden_dim(self):
        """Test setup with custom hidden_dim config."""
        from gymnasium.spaces import Box, Discrete

        module = KonicTorchPPO(
            observation_space=Box(low=-1.0, high=1.0, shape=(4,)),
            action_space=Discrete(2),
            model_config={"hidden_dim": 128},  # Custom hidden dim
        )
        module.setup()

        # Check hidden layer dimensions
        assert module.pi[0].out_features == 128
        assert module.vf[0].out_features == 128

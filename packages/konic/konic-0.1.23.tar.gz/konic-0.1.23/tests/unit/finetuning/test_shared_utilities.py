"""Tests for shared backend utilities."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import torch

from konic.finetuning.backends.capabilities import (
    DPO_CAPABILITIES,
    GRPO_CAPABILITIES,
    ONLINE_RL_CAPABILITIES,
    BackendCapabilities,
)
from konic.finetuning.config import GenerationConfig


class TestBackendCapabilities:
    """Tests for BackendCapabilities dataclass."""

    def test_default_capabilities(self):
        """Test default capability values."""
        caps = BackendCapabilities()
        assert caps.supports_online_generation is True
        assert caps.supports_offline_preference is False
        assert caps.requires_reward_composer is True
        assert caps.requires_value_head is True
        assert caps.supports_lora is True
        assert caps.supports_gradient_accumulation is True
        assert caps.supports_amp is True

    def test_custom_capabilities(self):
        """Test creating capabilities with custom values."""
        caps = BackendCapabilities(
            supports_online_generation=False,
            supports_offline_preference=True,
            requires_reward_composer=False,
            requires_value_head=False,
        )
        assert caps.supports_online_generation is False
        assert caps.supports_offline_preference is True
        assert caps.requires_reward_composer is False
        assert caps.requires_value_head is False

    def test_capabilities_are_frozen(self):
        """Test that capabilities are immutable."""
        caps = BackendCapabilities()
        with pytest.raises(Exception):  # FrozenInstanceError
            caps.supports_online_generation = False  # type: ignore[misc]

    def test_online_rl_capabilities(self):
        """Test predefined ONLINE_RL_CAPABILITIES."""
        assert ONLINE_RL_CAPABILITIES.supports_online_generation is True
        assert ONLINE_RL_CAPABILITIES.requires_reward_composer is True
        assert ONLINE_RL_CAPABILITIES.requires_value_head is True

    def test_grpo_capabilities(self):
        """Test predefined GRPO_CAPABILITIES."""
        assert GRPO_CAPABILITIES.supports_online_generation is True
        assert GRPO_CAPABILITIES.requires_reward_composer is True
        assert GRPO_CAPABILITIES.requires_value_head is False  # GRPO doesn't need value head

    def test_dpo_capabilities(self):
        """Test predefined DPO_CAPABILITIES."""
        assert DPO_CAPABILITIES.supports_online_generation is False
        assert DPO_CAPABILITIES.supports_offline_preference is True
        assert DPO_CAPABILITIES.requires_reward_composer is False


class TestGenerationUtility:
    """Tests for GenerationUtility class."""

    @pytest.fixture
    def mock_model(self):
        """Create a mock model."""
        model = MagicMock()
        model.generate.return_value = torch.tensor([[1, 2, 3, 4, 5, 6]])
        return model

    @pytest.fixture
    def mock_tokenizer(self):
        """Create a mock tokenizer."""
        tokenizer = MagicMock()
        tokenizer.return_value = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.tensor([[1, 1, 1]]),
        }
        tokenizer.batch_decode.return_value = ["generated response"]
        tokenizer.pad_token_id = 0
        return tokenizer

    def test_generation_utility_init(self, mock_model, mock_tokenizer):
        """Test GenerationUtility initialization."""
        from konic.finetuning.backends.shared.generation import GenerationUtility

        gen_config = GenerationConfig()
        utility = GenerationUtility(
            model=mock_model,
            tokenizer=mock_tokenizer,
            device="cpu",
            generation_config=gen_config,
        )

        assert utility._model is mock_model
        assert utility._tokenizer is mock_tokenizer
        assert utility._device == "cpu"

    def test_generation_utility_generate(self, mock_model, mock_tokenizer):
        """Test GenerationUtility.generate method."""
        from konic.finetuning.backends.shared.generation import GenerationUtility

        gen_config = GenerationConfig(max_new_tokens=50)
        utility = GenerationUtility(
            model=mock_model,
            tokenizer=mock_tokenizer,
            device="cpu",
            generation_config=gen_config,
        )

        prompts = ["test prompt"]
        result = utility.generate(prompts)

        assert result.responses == ["generated response"]
        assert result.input_ids is not None
        assert result.response_ids is not None
        mock_model.generate.assert_called_once()


class TestRewardComputationUtility:
    """Tests for RewardComputationUtility class."""

    @pytest.fixture
    def mock_composer(self):
        """Create a mock reward composer."""
        composer = MagicMock()
        composer.compose_batch.return_value = ([0.5, 0.8], {"score": [0.5, 0.8]})
        composer.compose.return_value = 0.6
        composer.get_reward_breakdown.return_value = {"score": 0.6}
        return composer

    def test_reward_utility_init(self, mock_composer):
        """Test RewardComputationUtility initialization."""
        from konic.finetuning.backends.shared.rewards import RewardComputationUtility

        utility = RewardComputationUtility(mock_composer)
        assert utility._composer is mock_composer

    def test_reward_utility_compute_batch(self, mock_composer):
        """Test batch reward computation."""
        from konic.finetuning.backends.shared.rewards import RewardComputationUtility

        utility = RewardComputationUtility(mock_composer)

        prompts = ["prompt1", "prompt2"]
        responses = ["response1", "response2"]

        rewards, breakdown = utility.compute(prompts, responses)

        assert rewards == [0.5, 0.8]
        assert "score" in breakdown
        mock_composer.compose_batch.assert_called_once_with(prompts, responses)

    def test_reward_utility_compute_sequential(self, mock_composer):
        """Test sequential reward computation when batch not available."""
        from konic.finetuning.backends.shared.rewards import RewardComputationUtility

        # Remove batch method
        del mock_composer.compose_batch

        utility = RewardComputationUtility(mock_composer)

        prompts = ["prompt1"]
        responses = ["response1"]

        rewards, breakdown = utility.compute(prompts, responses)

        assert len(rewards) == 1
        mock_composer.compose.assert_called_once()


class TestGenerationMixin:
    """Tests for GenerationMixin."""

    def test_mixin_provides_generate_method(self):
        """Test that mixin provides _generate_responses method."""
        from konic.finetuning.backends.shared.mixins import GenerationMixin

        class TestClass(GenerationMixin):
            def __init__(self):
                self._test_model = MagicMock()
                self._test_tokenizer = MagicMock()
                self._test_tokenizer.return_value = {
                    "input_ids": torch.tensor([[1, 2]]),
                    "attention_mask": torch.tensor([[1, 1]]),
                }
                self._test_tokenizer.batch_decode.return_value = ["response"]
                self._test_model.generate.return_value = torch.tensor([[1, 2, 3, 4]])

            def _get_model(self):
                return self._test_model

            def _get_tokenizer(self):
                return self._test_tokenizer

            def _get_device(self):
                return "cpu"

            def _get_generation_config(self):
                return GenerationConfig()

        obj = TestClass()
        responses, input_ids, response_ids = obj._generate_responses(["test"])

        assert responses == ["response"]
        assert input_ids is not None
        assert response_ids is not None


class TestRewardMixin:
    """Tests for RewardMixin."""

    def test_mixin_provides_compute_rewards_method(self):
        """Test that mixin provides _compute_rewards method."""
        from konic.finetuning.backends.shared.mixins import RewardMixin

        mock_composer = MagicMock()
        mock_composer.compose_batch.return_value = ([0.7], {"score": [0.7]})

        class TestClass(RewardMixin):
            def __init__(self, composer):
                self._composer = composer

            def _get_reward_composer(self):
                return self._composer

        obj = TestClass(mock_composer)
        rewards, breakdown = obj._compute_rewards(["prompt"], ["response"])

        assert rewards == [0.7]
        assert "score" in breakdown


class TestSharedModuleExports:
    """Tests for shared module exports."""

    def test_generation_module_exports(self):
        """Test generation module exports."""
        from konic.finetuning.backends.shared.generation import (
            GenerationOutput,
            GenerationUtility,
        )

        assert GenerationUtility is not None
        assert GenerationOutput is not None

    def test_rewards_module_exports(self):
        """Test rewards module exports."""
        from konic.finetuning.backends.shared.rewards import RewardComputationUtility

        assert RewardComputationUtility is not None

    def test_mixins_module_exports(self):
        """Test mixins module exports."""
        from konic.finetuning.backends.shared.mixins import GenerationMixin, RewardMixin

        assert GenerationMixin is not None
        assert RewardMixin is not None

    def test_capabilities_module_exports(self):
        """Test capabilities module exports."""
        from konic.finetuning.backends.capabilities import (
            DPO_CAPABILITIES,
            GRPO_CAPABILITIES,
            ONLINE_RL_CAPABILITIES,
            BackendCapabilities,
        )

        assert BackendCapabilities is not None
        assert ONLINE_RL_CAPABILITIES is not None
        assert GRPO_CAPABILITIES is not None
        assert DPO_CAPABILITIES is not None

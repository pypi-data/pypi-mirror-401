# pyright: reportAbstractUsage=false, reportArgumentType=false, reportOptionalMemberAccess=false
"""Tests for konic.finetuning.agent module."""

from unittest.mock import MagicMock

import pytest

from konic.common.errors import KonicConfigurationError
from konic.finetuning.agent import (
    BaseKonicFinetuningAgent,
    KonicFinetuningAgent,
)
from konic.finetuning.config import (
    GenerationConfig,
    KonicFinetuningMethodType,
    LoraConfig,
    TrainingConfig,
)


class TestBaseKonicFinetuningAgent:
    """Tests for BaseKonicFinetuningAgent abstract class."""

    def test_abstract_methods(self):
        # Verify all abstract methods are defined
        with pytest.raises(TypeError):
            BaseKonicFinetuningAgent()


class TestKonicFinetuningAgent:
    """Tests for KonicFinetuningAgent class."""

    def test_init_minimal(self):
        agent = KonicFinetuningAgent(base_model="test-model")

        assert agent._base_model == "test-model"
        assert agent._method == KonicFinetuningMethodType.NATIVE_PPO
        assert agent._environment is None
        assert agent._reward_composer is None
        assert agent._lora_config is None
        assert agent._dataset_config is None
        assert isinstance(agent._training_config, TrainingConfig)
        assert isinstance(agent._generation_config, GenerationConfig)

    def test_init_with_all_params(self):
        mock_env = MagicMock()
        mock_reward = MagicMock()
        mock_module = MagicMock()
        lora_config = LoraConfig(r=8)
        dataset_config = MagicMock()
        training_config = TrainingConfig(learning_rate=1e-4)
        generation_config = GenerationConfig(max_new_tokens=256)

        agent = KonicFinetuningAgent(
            base_model="test-model",
            environment=mock_env,
            reward_composer=mock_reward,
            module=mock_module,
            lora_config=lora_config,
            dataset_config=dataset_config,
            training_config=training_config,
            generation_config=generation_config,
            method=KonicFinetuningMethodType.NATIVE_PPO,
        )

        assert agent._base_model == "test-model"
        assert agent._environment is mock_env
        assert agent._reward_composer is mock_reward
        assert agent._module is mock_module
        assert agent._lora_config is lora_config
        assert agent._dataset_config is dataset_config
        assert agent._training_config is training_config
        assert agent._generation_config is generation_config

    def test_init_with_dict_training_config(self):
        agent = KonicFinetuningAgent(
            base_model="test-model",
            training_config={"learning_rate": 5e-5, "batch_size": 16},
        )

        assert agent._training_config.learning_rate == 5e-5
        assert agent._training_config.batch_size == 16

    def test_init_with_dict_generation_config(self):
        agent = KonicFinetuningAgent(
            base_model="test-model",
            generation_config={"max_new_tokens": 64, "temperature": 0.7},
        )

        assert agent._generation_config.max_new_tokens == 64
        assert agent._generation_config.temperature == 0.7

    def test_init_tracks_explicit_params(self):
        mock_env = MagicMock()
        mock_reward = MagicMock()
        mock_dataset = MagicMock()

        agent = KonicFinetuningAgent(
            base_model="test",
            environment=mock_env,
            reward_composer=mock_reward,
            dataset_config=mock_dataset,
        )

        assert agent._has_environment is True
        assert agent._has_reward_composer is True
        assert agent._has_dataset_config is True

        agent2 = KonicFinetuningAgent(base_model="test")
        assert agent2._has_environment is False
        assert agent2._has_reward_composer is False
        assert agent2._has_dataset_config is False

    def test_get_default_module_rlhf(self):
        agent = KonicFinetuningAgent(base_model="test")

        from konic.finetuning.module import KonicTorchRLHF

        assert agent._module is KonicTorchRLHF

    def test_get_base_model(self):
        agent = KonicFinetuningAgent(base_model="meta-llama/Llama-2-7b")
        assert agent.get_base_model() == "meta-llama/Llama-2-7b"

    def test_get_finetuning_method(self):
        agent = KonicFinetuningAgent(base_model="test")
        assert agent.get_finetuning_method() == KonicFinetuningMethodType.NATIVE_PPO

    def test_get_lora_config_with_config(self):
        lora = LoraConfig(r=32)
        agent = KonicFinetuningAgent(base_model="test", lora_config=lora)
        assert agent.get_lora_config() is lora

    def test_get_lora_config_none(self):
        agent = KonicFinetuningAgent(base_model="test")
        assert agent.get_lora_config() is None

    def test_get_reward_composer_raises_without_composer(self):
        agent = KonicFinetuningAgent(base_model="test")

        with pytest.raises(KonicConfigurationError) as exc_info:
            agent.get_reward_composer()

        assert "Reward composer is required" in str(exc_info.value)

    def test_get_reward_composer_with_composer(self):
        mock_reward = MagicMock()
        agent = KonicFinetuningAgent(base_model="test", reward_composer=mock_reward)
        assert agent.get_reward_composer() is mock_reward

    def test_get_dataset_config_raises_without_config(self):
        agent = KonicFinetuningAgent(base_model="test")

        with pytest.raises(KonicConfigurationError) as exc_info:
            agent.get_dataset_config()

        assert "Dataset configuration is required" in str(exc_info.value)

    def test_get_dataset_config_with_config(self):
        mock_dataset = MagicMock()
        agent = KonicFinetuningAgent(base_model="test", dataset_config=mock_dataset)
        assert agent.get_dataset_config() is mock_dataset

    def test_get_environment_raises_without_env(self):
        agent = KonicFinetuningAgent(base_model="test")

        with pytest.raises(KonicConfigurationError) as exc_info:
            agent.get_environment()

        assert "Environment is required" in str(exc_info.value)

    def test_get_environment_with_env(self):
        mock_env = MagicMock()
        agent = KonicFinetuningAgent(base_model="test", environment=mock_env)
        assert agent.get_environment() is mock_env

    def test_get_environment_config(self):
        gen_config = GenerationConfig(max_new_tokens=100, temperature=0.8)
        agent = KonicFinetuningAgent(
            base_model="test",
            generation_config=gen_config,
        )

        env_config = agent.get_environment_config()

        assert env_config["max_new_tokens"] == 100
        assert env_config["temperature"] == 0.8

    def test_get_algorithm_config(self):
        training_config = TrainingConfig(
            learning_rate=2e-5,
            clip_ratio=0.3,
            entropy_coef=0.02,
            vf_coef=0.6,
            max_grad_norm=0.5,
            gamma=0.99,
            gae_lambda=0.9,
        )
        agent = KonicFinetuningAgent(
            base_model="test",
            training_config=training_config,
        )

        algo_config = agent.get_algorithm_config()

        assert algo_config["learning_rate"] == 2e-5
        assert algo_config["clip_ratio"] == 0.3
        assert algo_config["entropy_coef"] == 0.02
        assert algo_config["vf_coef"] == 0.6
        assert algo_config["max_grad_norm"] == 0.5
        assert algo_config["gamma"] == 0.99
        assert algo_config["gae_lambda"] == 0.9

    def test_get_module(self):
        mock_module = MagicMock()
        agent = KonicFinetuningAgent(base_model="test", module=mock_module)
        assert agent.get_module() is mock_module

    def test_get_training_config(self):
        config = TrainingConfig(batch_size=16)
        agent = KonicFinetuningAgent(base_model="test", training_config=config)
        assert agent.get_training_config() is config

    def test_get_generation_config(self):
        config = GenerationConfig(temperature=0.5)
        agent = KonicFinetuningAgent(base_model="test", generation_config=config)
        assert agent.get_generation_config() is config

    def test_training_config_property(self):
        config = TrainingConfig(ppo_epochs=8)
        agent = KonicFinetuningAgent(base_model="test", training_config=config)
        assert agent.training_config is config

    def test_generation_config_property(self):
        config = GenerationConfig(top_p=0.9)
        agent = KonicFinetuningAgent(base_model="test", generation_config=config)
        assert agent.generation_config is config

    def test_default_module_with_custom_module(self):
        mock_module = MagicMock()
        agent = KonicFinetuningAgent(base_model="test", module=mock_module)

        # Custom module should override default
        assert agent._module is mock_module


class TestKonicFinetuningAgentIntegration:
    """Integration tests for KonicFinetuningAgent."""

    def test_full_configuration_workflow(self):
        from konic.finetuning.reward import KonicLLMRewardComposer, llm_reward

        class TestRewardComposer(KonicLLMRewardComposer):
            @llm_reward
            def length_reward(self, prompt: str, response: str) -> float:
                return min(len(response) / 100.0, 1.0)

        mock_dataset_config = MagicMock()
        mock_dataset_config.name = "test-dataset"

        agent = KonicFinetuningAgent(
            base_model="gpt2",
            reward_composer=TestRewardComposer(),
            dataset_config=mock_dataset_config,
            lora_config=LoraConfig(r=8),
            training_config=TrainingConfig(learning_rate=1e-4),
            generation_config=GenerationConfig(max_new_tokens=50),
        )

        # Verify all getters work
        assert agent.get_base_model() == "gpt2"
        assert isinstance(agent.get_reward_composer(), TestRewardComposer)
        assert agent.get_dataset_config() is mock_dataset_config
        assert agent.get_lora_config().r == 8
        assert agent.get_training_config().learning_rate == 1e-4
        assert agent.get_generation_config().max_new_tokens == 50

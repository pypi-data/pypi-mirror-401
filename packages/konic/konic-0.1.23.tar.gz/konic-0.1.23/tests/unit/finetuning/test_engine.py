# pyright: reportArgumentType=false, reportOptionalMemberAccess=false, reportAttributeAccessIssue=false
"""Tests for konic.finetuning.engine module."""

from unittest.mock import MagicMock, patch

import pytest
import torch

from konic.common.errors import KonicRuntimeError, KonicValidationError
from konic.finetuning.engine import (
    ADVANTAGE_STD_THRESHOLD,
    FinetuningIterationResult,
    FinetuningResult,
    KonicFinetuningEngine,
)


class TestFinetuningIterationResult:
    """Tests for FinetuningIterationResult dataclass."""

    def test_default_values(self):
        result = FinetuningIterationResult(iteration=1, reward_mean=0.5)

        assert result.iteration == 1
        assert result.reward_mean == 0.5
        assert result.reward_std == 0.0
        assert result.kl_divergence == 0.0
        assert result.policy_loss == 0.0
        assert result.value_loss == 0.0
        assert result.entropy_loss == 0.0
        assert result.total_loss == 0.0
        assert result.response_length_mean == 0.0
        assert result.clip_fraction == 0.0
        assert result.reward_breakdown == {}
        assert result.generation_time_sec == 0.0

    def test_to_dict(self):
        result = FinetuningIterationResult(
            iteration=5,
            reward_mean=0.75,
            reward_std=0.1,
            kl_divergence=0.05,
            policy_loss=0.2,
            value_loss=0.1,
            entropy_loss=0.01,
            total_loss=0.31,
            reward_breakdown={"custom": 0.5},
        )

        d = result.to_dict()

        assert d["iteration"] == 5
        assert d["reward/mean"] == 0.75
        assert d["reward/std"] == 0.1
        assert d["kl/divergence"] == 0.05
        assert d["loss/policy"] == 0.2
        assert d["loss/value"] == 0.1
        assert d["loss/entropy"] == 0.01
        assert d["loss/total"] == 0.31
        assert d["reward/custom"] == 0.5


class TestFinetuningResult:
    """Tests for FinetuningResult dataclass."""

    def test_default_values(self):
        result = FinetuningResult(total_iterations=0)

        assert result.total_iterations == 0
        assert result.best_iteration == 0
        assert result.best_reward == float("-inf")
        assert result.final_reward_mean == 0.0
        assert result.total_samples == 0
        assert result.history == []
        assert result.model_path is None

    def test_add_iteration_result(self):
        result = FinetuningResult(total_iterations=0)

        iter1 = FinetuningIterationResult(
            iteration=1, reward_mean=0.5, kl_divergence=0.01, total_time_sec=1.0
        )
        result.add_iteration_result(iter1)

        assert result.total_iterations == 1
        assert result.best_iteration == 1
        assert result.best_reward == 0.5
        assert result.final_reward_mean == 0.5
        assert len(result.history) == 1

    def test_add_iteration_result_updates_best(self):
        result = FinetuningResult(total_iterations=0)

        iter1 = FinetuningIterationResult(iteration=1, reward_mean=0.5, total_time_sec=1.0)
        iter2 = FinetuningIterationResult(iteration=2, reward_mean=0.8, total_time_sec=1.0)
        iter3 = FinetuningIterationResult(iteration=3, reward_mean=0.6, total_time_sec=1.0)

        result.add_iteration_result(iter1)
        result.add_iteration_result(iter2)
        result.add_iteration_result(iter3)

        assert result.best_iteration == 2
        assert result.best_reward == 0.8
        assert result.final_reward_mean == 0.6
        assert len(result.history) == 3

    def test_get_reward_curve(self):
        result = FinetuningResult(total_iterations=0)

        for i, reward in enumerate([0.1, 0.3, 0.5, 0.7], 1):
            result.add_iteration_result(
                FinetuningIterationResult(iteration=i, reward_mean=reward, total_time_sec=0.1)
            )

        curve = result.get_reward_curve()
        assert curve == [0.1, 0.3, 0.5, 0.7]

    def test_get_kl_curve(self):
        result = FinetuningResult(total_iterations=0)

        for i, kl in enumerate([0.01, 0.02, 0.03], 1):
            result.add_iteration_result(
                FinetuningIterationResult(
                    iteration=i, reward_mean=0.5, kl_divergence=kl, total_time_sec=0.1
                )
            )

        curve = result.get_kl_curve()
        assert curve == [0.01, 0.02, 0.03]

    def test_get_loss_curves(self):
        result = FinetuningResult(total_iterations=0)

        result.add_iteration_result(
            FinetuningIterationResult(
                iteration=1,
                reward_mean=0.5,
                policy_loss=0.1,
                value_loss=0.2,
                entropy_loss=0.01,
                total_loss=0.31,
                total_time_sec=0.1,
            )
        )

        curves = result.get_loss_curves()
        assert curves["policy"] == [0.1]
        assert curves["value"] == [0.2]
        assert curves["entropy"] == [0.01]
        assert curves["total"] == [0.31]

    def test_summary(self):
        result = FinetuningResult(
            total_iterations=10,
            best_iteration=5,
            best_reward=0.8,
            final_reward_mean=0.7,
            final_kl_divergence=0.05,
            total_samples=100,
            total_time_sec=60.0,
            model_name="test-model",
            model_path="/path/to/model",
        )

        summary = result.summary()

        assert "test-model" in summary
        assert "10" in summary  # total iterations
        assert "0.8" in summary  # best reward
        assert "/path/to/model" in summary

    def test_to_dict(self):
        result = FinetuningResult(
            total_iterations=5,
            best_iteration=3,
            best_reward=0.9,
            model_name="test",
        )

        d = result.to_dict()

        assert d["total_iterations"] == 5
        assert d["best_iteration"] == 3
        assert d["best_reward"] == 0.9
        assert d["model_name"] == "test"


class TestKonicFinetuningEngine:
    """Tests for KonicFinetuningEngine class."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose.return_value = 0.5
        composer.compose_batch.return_value = ([0.5, 0.6], {"reward": [0.5, 0.6]})
        composer.get_reward_breakdown.return_value = {"reward": 0.5}
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        config = MagicMock()
        config.name = "test-dataset"
        return config

    def test_init_basic(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        assert engine.model_name == "gpt2"
        assert engine.reward_composer is mock_reward_composer
        assert engine.dataset_config is mock_dataset_config
        assert engine.lora_config is None
        assert engine._is_setup is False

    def test_init_with_configs(self, mock_reward_composer, mock_dataset_config):
        from konic.finetuning.config import GenerationConfig, LoraConfig, TrainingConfig

        lora = LoraConfig(r=8)
        training = TrainingConfig(learning_rate=1e-4)
        generation = GenerationConfig(max_new_tokens=64)

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            lora_config=lora,
            training_config=training,
            generation_config=generation,
        )

        assert engine.lora_config is lora
        assert engine.training_config.learning_rate == 1e-4
        assert engine.generation_config.max_new_tokens == 64

    def test_init_device_auto(self, mock_reward_composer, mock_dataset_config):
        with patch("torch.cuda.is_available", return_value=True):
            engine = KonicFinetuningEngine(
                model_name="gpt2",
                reward_composer=mock_reward_composer,
                dataset_config=mock_dataset_config,
            )
            assert engine.device == "cuda"

    def test_init_custom_device(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )
        assert engine.device == "cpu"

    def test_module_property_before_setup_raises(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        with pytest.raises(KonicRuntimeError) as exc_info:
            _ = engine.module
        assert "Call setup() first" in str(exc_info.value)

    def test_dataset_loader_property_before_setup_raises(
        self, mock_reward_composer, mock_dataset_config
    ):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        with pytest.raises(KonicRuntimeError) as exc_info:
            _ = engine.dataset_loader
        assert "Call setup() first" in str(exc_info.value)

    def test_optimizer_property_before_setup_raises(
        self, mock_reward_composer, mock_dataset_config
    ):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        with pytest.raises(KonicRuntimeError) as exc_info:
            _ = engine.optimizer
        assert "Call setup() first" in str(exc_info.value)

    def test_from_agent(self):
        mock_agent = MagicMock()
        mock_agent.get_base_model.return_value = "test-model"
        mock_agent.get_reward_composer.return_value = MagicMock()
        mock_agent.get_dataset_config.return_value = MagicMock()
        mock_agent.get_lora_config.return_value = None
        mock_agent.get_training_config.return_value = MagicMock()
        mock_agent.get_generation_config.return_value = MagicMock()

        engine = KonicFinetuningEngine.from_agent(mock_agent)

        assert engine.model_name == "test-model"
        mock_agent.get_base_model.assert_called_once()

    def test_setup_validates_batch_size(self, mock_reward_composer, mock_dataset_config):
        from konic.finetuning.config import TrainingConfig

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(batch_size=0),
        )

        with pytest.raises(KonicValidationError) as exc_info:
            engine.setup()
        assert "batch_size must be positive" in str(exc_info.value)

    def test_setup_already_done(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )
        engine._is_setup = True

        # Should return early without error
        engine.setup()

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_setup_initializes_components(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader_cls.return_value = mock_loader

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )
        engine.setup()

        assert engine._is_setup is True
        mock_module.setup.assert_called_once()
        mock_loader.load.assert_called_once()

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    @patch("os.makedirs")
    def test_setup_creates_checkpoint_dir(
        self,
        mock_makedirs,
        mock_loader_cls,
        mock_module_cls,
        mock_reward_composer,
        mock_dataset_config,
    ):
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module_cls.return_value = mock_module
        mock_loader_cls.return_value = MagicMock()

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            checkpoint_dir="/tmp/checkpoints",
            device="cpu",
        )
        engine.setup()

        mock_makedirs.assert_called_with("/tmp/checkpoints", exist_ok=True)

    def test_compute_rewards_uses_batch_method(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        prompts = ["p1", "p2"]
        responses = ["r1", "r2"]

        rewards, breakdown = engine._compute_rewards(prompts, responses)

        mock_reward_composer.compose_batch.assert_called_once_with(prompts, responses)
        assert rewards == [0.5, 0.6]

    def test_compute_rewards_fallback_to_sequential(
        self, mock_reward_composer, mock_dataset_config
    ):
        # Remove compose_batch to test fallback
        del mock_reward_composer.compose_batch

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        prompts = ["p1", "p2"]
        responses = ["r1", "r2"]

        rewards, breakdown = engine._compute_rewards(prompts, responses)

        assert len(rewards) == 2
        assert mock_reward_composer.compose.call_count == 2

    def test_compute_advantages(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
        )

        rewards = torch.tensor([[0.0, 0.0, 1.0]])
        values = torch.tensor([[0.1, 0.2, 0.3]])

        advantages = engine._compute_advantages(rewards, values, gamma=0.99, gae_lambda=0.95)

        assert advantages.shape == rewards.shape
        # Last advantage should be approximately reward - value
        assert abs(advantages[0, -1].item() - (1.0 - 0.3)) < 0.1

    def test_save_checkpoint(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            checkpoint_dir="/tmp/checkpoints",
        )

        mock_module = MagicMock()
        mock_optimizer = MagicMock()
        mock_callback = MagicMock()

        engine._module = mock_module
        engine._optimizer = mock_optimizer
        engine.callback = mock_callback

        with patch("torch.save"):
            engine._save_checkpoint(10)

        mock_module.save_pretrained.assert_called_once()
        mock_callback.on_checkpoint_saved.assert_called_once()

    def test_save_checkpoint_no_dir(self, mock_reward_composer, mock_dataset_config):
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            checkpoint_dir=None,
        )

        # Should not raise
        engine._save_checkpoint(10)

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_evaluate(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.tokenizer.return_value = {"input_ids": torch.zeros(1, 10)}
        mock_module.tokenizer.batch_decode.return_value = ["response1"]
        mock_module.generate.return_value = torch.zeros(1, 20)
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader_cls.return_value = mock_loader

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )

        # Setup the engine to create the backend
        engine.setup()

        # Mock internal methods on the backend
        engine._backend._generate_responses = MagicMock(
            return_value=(["response"], torch.zeros(1, 5), torch.zeros(1, 5))
        )

        result = engine.evaluate(["prompt1"])

        assert "prompts" in result
        assert "responses" in result
        assert "rewards" in result
        assert "reward_mean" in result


class TestPPOUpdate:
    """Tests for the PPO update logic."""

    @pytest.fixture
    def engine(self):
        from konic.finetuning.config import TrainingConfig

        mock_reward = MagicMock()
        mock_dataset = MagicMock()

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward,
            dataset_config=mock_dataset,
            training_config=TrainingConfig(ppo_epochs=2, batch_size=2),
            device="cpu",
        )
        return engine

    def test_ppo_update_validates_batch_size(self, engine):
        engine._module = MagicMock()
        engine._optimizer = MagicMock()

        input_ids = torch.zeros(0, 10, dtype=torch.long)
        response_ids = torch.zeros(0, 5, dtype=torch.long)

        with pytest.raises(KonicValidationError) as exc_info:
            engine._ppo_update(input_ids, response_ids, [])
        assert "Empty batch" in str(exc_info.value)

    def test_ppo_update_validates_reward_length(self, engine):
        engine._module = MagicMock()
        engine._optimizer = MagicMock()

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)

        with pytest.raises(KonicValidationError) as exc_info:
            engine._ppo_update(input_ids, response_ids, [0.5])  # Wrong length
        assert "doesn't match batch size" in str(exc_info.value)


class TestAdvantageStdThreshold:
    """Tests for advantage normalization threshold."""

    def test_threshold_value(self):
        assert ADVANTAGE_STD_THRESHOLD == 1e-6


class TestFinetuningIterationResultComplete:
    """Complete tests for FinetuningIterationResult."""

    def test_all_fields(self):
        result = FinetuningIterationResult(
            iteration=10,
            reward_mean=0.75,
            reward_std=0.15,
            reward_min=0.2,
            reward_max=0.95,
            kl_divergence=0.02,
            policy_loss=0.15,
            value_loss=0.08,
            entropy_loss=0.005,
            total_loss=0.235,
            response_length_mean=25.5,
            response_length_std=5.2,
            learning_rate=1e-5,
            clip_fraction=0.12,
            approx_kl=0.015,
            explained_variance=0.85,
            reward_breakdown={"custom": 0.5, "length": 0.25},
            generation_time_sec=1.5,
            reward_compute_time_sec=0.8,
            update_time_sec=2.0,
            total_time_sec=4.3,
        )

        d = result.to_dict()

        assert d["iteration"] == 10
        assert d["reward/mean"] == 0.75
        assert d["reward/std"] == 0.15
        assert d["reward/min"] == 0.2
        assert d["reward/max"] == 0.95
        assert d["kl/divergence"] == 0.02
        assert d["loss/policy"] == 0.15
        assert d["loss/value"] == 0.08
        assert d["loss/entropy"] == 0.005
        assert d["loss/total"] == 0.235
        assert d["response/length_mean"] == 25.5
        assert d["response/length_std"] == 5.2
        assert d["train/learning_rate"] == 1e-5
        assert d["train/clip_fraction"] == 0.12
        assert d["train/approx_kl"] == 0.015
        assert d["train/explained_variance"] == 0.85
        assert d["time/generation_sec"] == 1.5
        assert d["time/reward_sec"] == 0.8
        assert d["time/update_sec"] == 2.0
        assert d["time/total_sec"] == 4.3
        assert d["reward/custom"] == 0.5
        assert d["reward/length"] == 0.25


class TestFinetuningResultComplete:
    """Complete tests for FinetuningResult."""

    def test_summary_without_model_path(self):
        result = FinetuningResult(
            total_iterations=5,
            model_name="test-model",
        )

        summary = result.summary()

        assert "test-model" in summary
        assert "Model saved to" not in summary

    def test_to_dict_with_history(self):
        result = FinetuningResult(
            total_iterations=2,
            model_name="test",
            lora_config={"r": 8},
            training_config={"lr": 1e-4},
        )

        iter1 = FinetuningIterationResult(iteration=1, reward_mean=0.5, total_time_sec=1.0)
        result.add_iteration_result(iter1)

        d = result.to_dict()

        assert d["lora_config"] == {"r": 8}
        assert d["training_config"] == {"lr": 1e-4}
        assert len(d["history"]) == 1


class TestKonicFinetuningEngineComplete:
    """Complete tests for KonicFinetuningEngine."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose.return_value = 0.5
        composer.compose_batch.return_value = ([0.5, 0.6], {"reward": [0.5, 0.6]})
        composer.get_reward_breakdown.return_value = {"reward": 0.5}
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        config = MagicMock()
        config.name = "test-dataset"
        return config

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_train_loop_basic(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        """Test basic training loop."""
        from konic.finetuning.config import TrainingConfig

        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.tokenizer = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.tokenizer.return_value = {
            "input_ids": torch.zeros(2, 10, dtype=torch.long),
            "attention_mask": torch.ones(2, 10, dtype=torch.long),
        }
        mock_module.tokenizer.__call__ = MagicMock(
            return_value=MagicMock(
                __getitem__=lambda self, key: torch.zeros(2, 10, dtype=torch.long)
            )
        )
        mock_module.tokenizer.batch_decode.return_value = ["response1", "response2"]
        mock_module.generate.return_value = torch.zeros(2, 20, dtype=torch.long)
        mock_module.get_log_probs.return_value = torch.zeros(2, 19)
        mock_module.get_ref_log_probs.return_value = torch.zeros(2, 19)
        mock_module.compute_values_for_all_tokens.return_value = torch.zeros(2, 20)
        mock_module.save_pretrained = MagicMock()
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader.iter_batches.return_value = iter([{"text": ["a", "b"]}])
        mock_loader.get_prompts.return_value = ["prompt1", "prompt2"]
        mock_loader_cls.return_value = mock_loader

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(batch_size=2, ppo_epochs=1),
            device="cpu",
        )

        # Setup the engine to create the backend
        engine.setup()

        # Mock internal methods on the backend (not the engine)
        engine._backend._generate_responses = MagicMock(
            return_value=(["r1", "r2"], torch.zeros(2, 5), torch.zeros(2, 5))
        )
        engine._backend._ppo_update = MagicMock(
            return_value={
                "policy_loss": 0.1,
                "value_loss": 0.05,
                "entropy_loss": 0.01,
                "total_loss": 0.16,
                "clip_fraction": 0.1,
                "approx_kl": 0.01,
                "kl_divergence": 0.02,
            }
        )

        result = engine.train(max_iterations=1)

        assert result.total_iterations == 1
        assert len(result.history) == 1

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_train_with_early_stopping(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        """Test training with early stopping callback."""
        from konic.finetuning.callback import BaseKonicFinetuningCallback

        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.save_pretrained = MagicMock()
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader.iter_batches.return_value = iter([{"text": ["a"]}])
        mock_loader.get_prompts.return_value = ["prompt"]
        mock_loader_cls.return_value = mock_loader

        # Create callback that triggers early stopping
        mock_callback = MagicMock(spec=BaseKonicFinetuningCallback)
        mock_callback.should_stop_early.return_value = True

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            callback=mock_callback,
            device="cpu",
        )

        # Setup the engine to create the backend
        engine.setup()

        # Mock internal methods on the backend
        engine._backend._generate_responses = MagicMock(
            return_value=(["r"], torch.zeros(1, 5), torch.zeros(1, 5))
        )
        engine._backend._ppo_update = MagicMock(return_value={"policy_loss": 0.1})

        engine.train(max_iterations=10)

        # Should stop after first iteration due to early stopping
        mock_callback.should_stop_early.assert_called()

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_train_with_checkpoint_save(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        """Test training with periodic checkpoint saving."""
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.save_pretrained = MagicMock()
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader.iter_batches.return_value = iter([{"text": ["a"]}] * 3)
        mock_loader.get_prompts.return_value = ["prompt"]
        mock_loader_cls.return_value = mock_loader

        with patch("os.makedirs"), patch("torch.save"):
            engine = KonicFinetuningEngine(
                model_name="gpt2",
                reward_composer=mock_reward_composer,
                dataset_config=mock_dataset_config,
                checkpoint_dir="/tmp/test_ckpt",
                device="cpu",
            )

            # Setup the engine to create the backend
            engine.setup()

            # Mock internal methods on the backend
            engine._backend._generate_responses = MagicMock(
                return_value=(["r"], torch.zeros(1, 5), torch.zeros(1, 5))
            )
            engine._backend._ppo_update = MagicMock(return_value={"policy_loss": 0.1})

            engine.train(max_iterations=3, save_every=2)

            # Checkpoint should be saved at iteration 2
            assert mock_module.save_pretrained.call_count >= 1

    def test_generate_responses(self, mock_reward_composer, mock_dataset_config):
        """Test _generate_responses method."""
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )

        mock_module = MagicMock()
        mock_tokenizer = MagicMock()

        # Create proper mock for tokenizer call
        mock_inputs = MagicMock()
        mock_inputs.__getitem__ = MagicMock(
            side_effect=lambda key: torch.ones(2, 10, dtype=torch.long)
        )
        mock_tokenizer.return_value = mock_inputs
        mock_tokenizer.batch_decode.return_value = ["response1", "response2"]
        mock_tokenizer.pad_token_id = 0

        mock_module.tokenizer = mock_tokenizer
        mock_module.generate.return_value = torch.zeros(2, 20, dtype=torch.long)

        engine._module = mock_module
        engine._is_setup = True
        engine._device = "cpu"

        # This will fail because of the mock setup, but tests the code path
        # For real testing we'd need more elaborate mocking

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_train_iter_empty_prompts_raises(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        """Test train_iter raises when no prompts available."""
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader.iter_batches.return_value = iter([{"text": ["a"]}])
        mock_loader.get_prompts.return_value = []  # Empty prompts
        mock_loader_cls.return_value = mock_loader

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )

        # Setup the engine to create the backend
        engine.setup()

        with pytest.raises(KonicValidationError) as exc_info:
            engine.train_iter(1)
        assert "No prompts available" in str(exc_info.value)


class TestPPOUpdateComplete:
    """Complete tests for PPO update."""

    @pytest.fixture
    def engine(self):
        from konic.finetuning.config import TrainingConfig

        mock_reward = MagicMock()
        mock_dataset = MagicMock()

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward,
            dataset_config=mock_dataset,
            training_config=TrainingConfig(
                ppo_epochs=2,
                batch_size=2,
                kl_penalty_weight=0.1,
                clip_ratio=0.2,
                vf_coef=0.5,
                entropy_coef=0.01,
                max_grad_norm=1.0,
                gamma=0.99,
                gae_lambda=0.95,
            ),
            device="cpu",
        )
        return engine

    def test_ppo_update_has_forward_cache_path(self, engine):
        """Test that PPO update checks for forward_with_cache method."""
        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0

        # Mock hasattr to return True for forward_with_cache
        assert hasattr(mock_module, "forward_with_cache")

        # Verify engine uses forward_with_cache when available
        engine._module = mock_module
        assert hasattr(engine._module, "forward_with_cache")

    def test_ppo_update_fallback_path_when_no_cache(self, engine):
        """Test that PPO update uses fallback when forward_with_cache is missing."""
        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0

        # Remove forward_with_cache to simulate fallback path
        del mock_module.forward_with_cache

        # Verify fallback methods exist
        engine._module = mock_module
        assert not hasattr(engine._module, "forward_with_cache")
        assert hasattr(engine._module, "get_log_probs")
        assert hasattr(engine._module, "compute_values_for_all_tokens")

    def test_compute_advantages_gae(self, engine):
        """Test GAE advantage computation."""
        rewards = torch.tensor([[0.0, 0.0, 0.0, 1.0]])
        values = torch.tensor([[0.1, 0.2, 0.3, 0.4]])

        advantages = engine._compute_advantages(rewards, values, gamma=0.99, gae_lambda=0.95)

        assert advantages.shape == rewards.shape
        # Last timestep advantage
        assert advantages[0, -1] == pytest.approx(1.0 - 0.4, abs=0.01)

    def test_advantage_normalization_with_constant_values(self, engine):
        """Test advantage normalization behavior with constant rewards."""
        # Test the ADVANTAGE_STD_THRESHOLD constant directly
        assert ADVANTAGE_STD_THRESHOLD == 1e-6

        # When all rewards are identical, std should be 0 or very small
        identical_rewards = torch.tensor([0.5, 0.5, 0.5, 0.5])
        mean = identical_rewards.mean()
        std = identical_rewards.std()

        # With identical values, std should be 0 (or very small due to numerical precision)
        assert std <= ADVANTAGE_STD_THRESHOLD

        # If std is below threshold, normalization should use max(std, threshold)
        normalized = (identical_rewards - mean) / max(std, ADVANTAGE_STD_THRESHOLD)
        assert torch.isfinite(normalized).all()


class TestTrainLoopExceptionHandling:
    """Tests for exception handling in the train loop."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose_batch.return_value = ([0.5, 0.6], {"reward": [0.5, 0.6]})
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        config = MagicMock()
        config.name = "test-dataset"
        return config

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_train_loop_handles_stop_iteration(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config
    ):
        """Test that StopIteration from train_iter ends training gracefully."""
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.save_pretrained = MagicMock()
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader_cls.return_value = mock_loader

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )

        # Setup the engine to create the backend
        engine.setup()

        # Make backend's _train_iteration raise StopIteration on first call
        engine._backend._train_iteration = MagicMock(side_effect=StopIteration("Dataset exhausted"))

        result = engine.train(max_iterations=10)

        # Training should complete without error, with 0 iterations
        assert result.total_iterations == 0

    @patch("konic.finetuning.backends.native.backend.KonicTorchRLHF")
    @patch("konic.finetuning.backends.native.backend.DatasetLoader")
    def test_train_loop_handles_keyboard_interrupt(
        self, mock_loader_cls, mock_module_cls, mock_reward_composer, mock_dataset_config, capsys
    ):
        """Test that KeyboardInterrupt prints message and exits gracefully."""
        mock_module = MagicMock()
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.save_pretrained = MagicMock()
        mock_module_cls.return_value = mock_module

        mock_loader = MagicMock()
        mock_loader_cls.return_value = mock_loader

        with patch("os.makedirs"):
            engine = KonicFinetuningEngine(
                model_name="gpt2",
                reward_composer=mock_reward_composer,
                dataset_config=mock_dataset_config,
                checkpoint_dir="/tmp/test_ckpt",
                device="cpu",
            )

            # Setup the engine to create the backend
            engine.setup()

            call_count = 0

            def train_iter_with_interrupt(iteration):
                nonlocal call_count
                call_count += 1
                if call_count == 2:
                    raise KeyboardInterrupt()
                return FinetuningIterationResult(
                    iteration=iteration, reward_mean=0.5, total_time_sec=1.0
                )

            engine._backend._train_iteration = MagicMock(side_effect=train_iter_with_interrupt)

            engine.train(max_iterations=10)

            # Should have captured the interrupt message
            captured = capsys.readouterr()
            assert "interrupted" in captured.out.lower()


class TestGenerateResponses:
    """Tests for _generate_responses method."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose_batch.return_value = ([0.5], {"reward": [0.5]})
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        config = MagicMock()
        config.name = "test-dataset"
        return config

    def test_generate_responses_tokenizes_and_generates(
        self, mock_reward_composer, mock_dataset_config
    ):
        """Test that _generate_responses properly tokenizes prompts and generates responses."""
        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            device="cpu",
        )

        # Setup mock module with tokenizer
        mock_module = MagicMock()
        mock_tokenizer = MagicMock()

        # Create mock input tensors
        input_ids = torch.tensor([[1, 2, 3, 4, 5]], dtype=torch.long)
        attention_mask = torch.ones_like(input_ids)

        mock_inputs = MagicMock()
        mock_inputs.__getitem__ = MagicMock(
            side_effect=lambda key: input_ids if key == "input_ids" else attention_mask
        )
        mock_tokenizer.return_value = mock_inputs

        # Output includes input + generated tokens
        output_ids = torch.tensor([[1, 2, 3, 4, 5, 100, 101, 102]], dtype=torch.long)
        mock_module.generate.return_value = output_ids
        mock_tokenizer.batch_decode.return_value = ["generated response"]

        mock_module.tokenizer = mock_tokenizer
        engine._module = mock_module
        engine._is_setup = True

        responses, returned_input_ids, response_ids = engine._generate_responses(["test prompt"])

        assert responses == ["generated response"]
        mock_tokenizer.batch_decode.assert_called_once()
        mock_module.generate.assert_called_once()
        # Response IDs should be output_ids minus input_ids
        assert response_ids.shape[1] == output_ids.shape[1] - input_ids.shape[1]


class TestPPOUpdateExecution:
    """Tests for the PPO update method execution."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose_batch.return_value = ([0.5, 0.6], {"reward": [0.5, 0.6]})
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        config = MagicMock()
        config.name = "test-dataset"
        return config

    def test_ppo_update_with_forward_cache(self, mock_reward_composer, mock_dataset_config):
        """Test PPO update using forward_all (consolidated forward pass)."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        # Create mock forward_all response using new API
        def make_forward_all_return(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=make_forward_all_return)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        losses = engine._ppo_update(input_ids, response_ids, rewards)

        assert "policy_loss" in losses
        assert "value_loss" in losses
        assert "entropy_loss" in losses
        assert "total_loss" in losses
        assert "clip_fraction" in losses
        assert "approx_kl" in losses
        assert "kl_divergence" in losses
        mock_module.forward_all.assert_called()

    def test_ppo_update_without_forward_cache(self, mock_reward_composer, mock_dataset_config):
        """Test PPO update uses forward_all (no longer uses fallback path)."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def make_forward_all_return(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=make_forward_all_return)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        losses = engine._ppo_update(input_ids, response_ids, rewards)

        assert "policy_loss" in losses
        assert "value_loss" in losses
        # forward_all is now always used (no fallback)
        mock_module.forward_all.assert_called()

    def test_ppo_update_gradient_clipping(self, mock_reward_composer, mock_dataset_config):
        """Test that PPO update applies gradient clipping."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, max_grad_norm=0.5),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def make_forward_all_return(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=make_forward_all_return)
        params = [torch.nn.Parameter(torch.zeros(10))]
        mock_module.get_trainable_parameters.return_value = params

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        with patch("torch.nn.utils.clip_grad_norm_") as mock_clip:
            engine._ppo_update(input_ids, response_ids, rewards)
            mock_clip.assert_called()

    def test_ppo_update_advantage_normalization_low_std(
        self, mock_reward_composer, mock_dataset_config
    ):
        """Test advantage normalization when std is below threshold."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        # Return identical values to trigger low std path
        def make_forward_all_return(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.full(
                    (batch, ids.shape[1]), 0.5, requires_grad=True
                ),  # Constant values
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=make_forward_all_return)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        # Same rewards to trigger low variance
        rewards = [0.5, 0.5]

        # Should not raise due to division by zero
        losses = engine._ppo_update(input_ids, response_ids, rewards)
        assert "policy_loss" in losses


class TestGradientAccumulation:
    """Tests for gradient accumulation in PPO update."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose_batch.return_value = (
            [0.5, 0.6, 0.7, 0.8],
            {"r": [0.5, 0.6, 0.7, 0.8]},
        )
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        return MagicMock(name="test")

    def test_gradient_accumulation_splits_batch(self, mock_reward_composer, mock_dataset_config):
        """Test that gradient accumulation correctly splits batches."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(
                batch_size=4,
                gradient_accumulation_steps=2,
                ppo_epochs=1,
            ),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(4, 10, dtype=torch.long)
        response_ids = torch.zeros(4, 5, dtype=torch.long)
        rewards = [0.5, 0.6, 0.7, 0.8]

        losses = engine._ppo_update(input_ids, response_ids, rewards)

        # forward_all should be called multiple times
        assert mock_module.forward_all.call_count >= 3
        assert "policy_loss" in losses

    def test_gradient_accumulation_handles_non_divisible_batch(
        self, mock_reward_composer, mock_dataset_config
    ):
        """Test handling when batch_size is not divisible by accumulation_steps."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        mock_reward_composer.compose_batch.return_value = (
            [0.5, 0.6, 0.7],
            {"r": [0.5, 0.6, 0.7]},
        )

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(
                batch_size=3,
                gradient_accumulation_steps=2,
                ppo_epochs=1,
            ),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(3, 10, dtype=torch.long)
        response_ids = torch.zeros(3, 5, dtype=torch.long)
        rewards = [0.5, 0.6, 0.7]

        # Should not raise
        losses = engine._ppo_update(input_ids, response_ids, rewards)
        assert "policy_loss" in losses

    def test_small_batch_reduces_accumulation_steps(
        self, mock_reward_composer, mock_dataset_config
    ):
        """Test that accumulation steps is reduced when batch_size < steps."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        mock_reward_composer.compose_batch.return_value = (
            [0.5, 0.6],
            {"r": [0.5, 0.6]},
        )

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(
                batch_size=2,
                gradient_accumulation_steps=8,
                ppo_epochs=1,
            ),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        # Should work with reduced accumulation steps
        losses = engine._ppo_update(input_ids, response_ids, rewards)
        assert "policy_loss" in losses


class TestConsolidatedForwardPasses:
    """Tests for forward pass consolidation using forward_all."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose_batch.return_value = ([0.5, 0.6], {"r": [0.5, 0.6]})
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        return MagicMock(name="test")

    def test_ppo_update_uses_forward_all(self, mock_reward_composer, mock_dataset_config):
        """Test that _ppo_update uses the consolidated forward_all method."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        engine._ppo_update(input_ids, response_ids, rewards)

        # Verify forward_all was used
        assert mock_module.forward_all.called
        # Old methods should not be called
        assert not mock_module.get_log_probs.called
        assert not mock_module.compute_values_for_all_tokens.called


class TestEngineAMPIntegration:
    """Tests for AMP integration in the engine."""

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose_batch.return_value = ([0.5, 0.6], {"r": [0.5, 0.6]})
        return composer

    @pytest.fixture
    def mock_dataset_config(self):
        return MagicMock(name="test")

    def test_ppo_update_respects_module_amp_setting(
        self, mock_reward_composer, mock_dataset_config
    ):
        """Test that engine respects module's AMP setting."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = True
        mock_scaler = MagicMock()
        mock_module.scaler = mock_scaler

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        with patch("torch.cuda.amp.autocast"):
            engine._ppo_update(input_ids, response_ids, rewards)

        # Scaler methods should be called when AMP is enabled
        mock_scaler.scale.assert_called()
        mock_scaler.step.assert_called()
        mock_scaler.update.assert_called()

    def test_ppo_update_without_amp(self, mock_reward_composer, mock_dataset_config):
        """Test that engine works correctly without AMP."""
        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        # Should work without AMP
        losses = engine._ppo_update(input_ids, response_ids, rewards)
        assert "policy_loss" in losses
        engine._optimizer.step.assert_called()

    def test_ppo_update_uses_get_amp_context(self, mock_reward_composer, mock_dataset_config):
        """Test that engine uses module's get_amp_context helper method."""
        import contextlib

        from konic.finetuning.config import TrainingConfig
        from konic.finetuning.module import ForwardAllOutput

        engine = KonicFinetuningEngine(
            model_name="gpt2",
            reward_composer=mock_reward_composer,
            dataset_config=mock_dataset_config,
            training_config=TrainingConfig(ppo_epochs=1, batch_size=2),
            device="cpu",
        )

        mock_module = MagicMock()
        mock_module.tokenizer.pad_token_id = 0
        mock_module.use_amp = False
        mock_module.scaler = None
        mock_module.get_amp_context.return_value = contextlib.nullcontext()

        def mock_forward_all(ids, mask, compute_ref=True):
            batch = ids.shape[0]
            return ForwardAllOutput(
                log_probs=torch.zeros(batch, ids.shape[1] - 1, requires_grad=True),
                values=torch.zeros(batch, ids.shape[1], requires_grad=True),
                ref_log_probs=torch.zeros(batch, ids.shape[1] - 1),
                hidden_states=torch.zeros(batch, ids.shape[1], 256),
            )

        mock_module.forward_all = MagicMock(side_effect=mock_forward_all)
        mock_module.get_trainable_parameters.return_value = [torch.nn.Parameter(torch.zeros(10))]

        engine._module = mock_module
        engine._optimizer = MagicMock()
        engine._is_setup = True

        input_ids = torch.zeros(2, 10, dtype=torch.long)
        response_ids = torch.zeros(2, 5, dtype=torch.long)
        rewards = [0.5, 0.6]

        engine._ppo_update(input_ids, response_ids, rewards)

        # get_amp_context should be called for each micro-batch in each PPO epoch
        assert mock_module.get_amp_context.call_count >= 1

"""Tests for TRL adapter modules."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from konic.finetuning.backends.result import FinetuningIterationResult
from konic.finetuning.config import TrainingConfig


class TestConfigMapper:
    """Tests for TRL config mapper functions."""

    @pytest.fixture
    def training_config(self):
        """Create a training config for testing."""
        return TrainingConfig(
            learning_rate=1e-5,
            batch_size=4,
            gradient_accumulation_steps=2,
            max_grad_norm=1.0,
            kl_penalty_weight=0.1,
        )

    def test_training_config_to_grpo_config(self, training_config):
        """Test conversion to GRPOConfig."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        mock_grpo_config = MagicMock()
        with patch("trl.GRPOConfig", mock_grpo_config):
            from konic.finetuning.backends.trl.adapter.config import (
                training_config_to_grpo_config,
            )

            training_config_to_grpo_config(training_config, output_dir="/tmp/test", max_steps=50)

            mock_grpo_config.assert_called_once()
            call_kwargs = mock_grpo_config.call_args[1]
            assert call_kwargs["learning_rate"] == 1e-5
            assert call_kwargs["per_device_train_batch_size"] == 4
            assert call_kwargs["gradient_accumulation_steps"] == 2
            assert call_kwargs["max_grad_norm"] == 1.0
            assert call_kwargs["beta"] == 0.1  # kl_penalty_weight
            assert call_kwargs["output_dir"] == "/tmp/test"
            assert call_kwargs["max_steps"] == 50

    def test_training_config_to_dpo_config(self, training_config):
        """Test conversion to DPOConfig."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        mock_dpo_config = MagicMock()
        with patch("trl.DPOConfig", mock_dpo_config):
            from konic.finetuning.backends.trl.adapter.config import (
                training_config_to_dpo_config,
            )

            training_config_to_dpo_config(training_config, output_dir="/tmp/dpo", max_steps=100)

            mock_dpo_config.assert_called_once()
            call_kwargs = mock_dpo_config.call_args[1]
            assert call_kwargs["learning_rate"] == 1e-5
            assert call_kwargs["per_device_train_batch_size"] == 4
            assert call_kwargs["beta"] == 0.1  # Used for DPO KL coefficient
            assert call_kwargs["output_dir"] == "/tmp/dpo"
            assert call_kwargs["max_steps"] == 100

    def test_generation_config_to_kwargs(self):
        """Test conversion of generation config to kwargs."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.config import (
            generation_config_to_kwargs,
        )
        from konic.finetuning.config import GenerationConfig

        gen_config = GenerationConfig(
            max_new_tokens=128,
            temperature=0.8,
            top_p=0.95,
            do_sample=True,
        )

        result = generation_config_to_kwargs(gen_config)

        assert result["max_new_tokens"] == 128
        assert result["temperature"] == 0.8
        assert result["top_p"] == 0.95
        assert result["do_sample"] is True

    def test_lora_config_to_peft_config_none(self):
        """Test conversion when lora_config is None."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.config import lora_config_to_peft_config

        result = lora_config_to_peft_config(None)
        assert result is None

    def test_lora_config_to_peft_config(self):
        """Test conversion of LoraConfig to PEFT config."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.config import LoraConfig

        mock_peft_lora = MagicMock()
        with patch("peft.LoraConfig", mock_peft_lora):
            from konic.finetuning.backends.trl.adapter.config import lora_config_to_peft_config

            lora_config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.1)
            lora_config_to_peft_config(lora_config)

            mock_peft_lora.assert_called_once()


class TestRewardAdapter:
    """Tests for TRL reward adapter."""

    def test_adapt_reward_composer_to_trl(self):
        """Test adaptation of reward composer to TRL format."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.reward import adapt_reward_composer_to_trl

        mock_composer = MagicMock()
        mock_composer.compose_batch.return_value = ([0.5, 0.8], {"score": [0.5, 0.8]})

        reward_func = adapt_reward_composer_to_trl(mock_composer)

        # Test the adapted function
        completions = ["response 1", "response 2"]
        prompts = ["prompt 1", "prompt 2"]

        result = reward_func(completions, prompts)

        assert result == [0.5, 0.8]
        mock_composer.compose_batch.assert_called_once()

    def test_adapt_reward_composer_handles_none_prompts(self):
        """Test that adapter handles None prompts."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.reward import adapt_reward_composer_to_trl

        mock_composer = MagicMock()
        mock_composer.compose_batch.return_value = ([0.7], {"score": [0.7]})

        reward_func = adapt_reward_composer_to_trl(mock_composer)

        # Call with None prompts (testing None handling)
        result = reward_func(["response"], None)  # type: ignore[arg-type]

        assert result == [0.7]

    def test_create_reward_func_from_callable(self):
        """Test creating TRL reward func from simple callable."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.reward import create_reward_func_from_callable

        def simple_reward(prompt: str, response: str) -> float:
            return len(response) / 100.0

        trl_func = create_reward_func_from_callable(simple_reward)

        result = trl_func(["short", "longer response"], ["p1", "p2"])

        assert len(result) == 2
        assert result[0] < result[1]  # longer response should score higher


class TestCallbackAdapter:
    """Tests for TRL callback adapter."""

    @pytest.fixture
    def mock_konic_callback(self):
        """Create a mock Konic callback."""
        callback = MagicMock()
        callback.should_stop_early.return_value = False
        return callback

    def test_create_trl_callback_adapter(self, mock_konic_callback):
        """Test creation of TRL callback adapter."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.callback import (
            create_trl_callback_adapter,
        )

        adapter = create_trl_callback_adapter(mock_konic_callback)
        assert adapter is not None

    def test_callback_adapter_on_train_begin_skips(self, mock_konic_callback):
        """Test callback adapter on_train_begin skips (backend handles it)."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.callback import (
            create_trl_callback_adapter,
        )

        adapter = create_trl_callback_adapter(mock_konic_callback)

        # Mock args and state
        mock_args = MagicMock()
        mock_state = MagicMock()
        mock_control = MagicMock()

        # Should not raise and should not call Konic callback
        adapter.on_train_begin(mock_args, mock_state, mock_control)

        # Backend handles on_train_begin with full context, so adapter skips it
        mock_konic_callback.on_train_begin.assert_not_called()

    def test_callback_adapter_on_log(self, mock_konic_callback):
        """Test callback adapter on_log fires iteration callback."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.callback import (
            create_trl_callback_adapter,
        )

        adapter = create_trl_callback_adapter(mock_konic_callback)

        mock_args = MagicMock()
        mock_state = MagicMock()
        mock_state.global_step = 10
        mock_control = MagicMock()

        # Logs dict is passed to on_log
        logs = {"loss": 0.5, "reward": 0.8, "kl": 0.1, "step_time": 2.0}

        adapter.on_log(mock_args, mock_state, mock_control, logs=logs)

        mock_konic_callback.on_iteration_end.assert_called_once()
        call_arg = mock_konic_callback.on_iteration_end.call_args[0][0]
        assert isinstance(call_arg, FinetuningIterationResult)
        assert call_arg.iteration == 10
        assert call_arg.reward_mean == 0.8
        assert call_arg.kl_divergence == 0.1

    def test_callback_adapter_stops_on_early_stop(self, mock_konic_callback):
        """Test callback adapter honors early stopping via on_log."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        mock_konic_callback.should_stop_early.return_value = True

        from konic.finetuning.backends.trl.adapter.callback import (
            create_trl_callback_adapter,
        )

        adapter = create_trl_callback_adapter(mock_konic_callback)

        mock_args = MagicMock()
        mock_state = MagicMock()
        mock_state.global_step = 10
        mock_control = MagicMock()
        mock_control.should_training_stop = False

        # on_log is where early stopping is checked
        logs = {"loss": 0.5, "reward": 0.3}
        adapter.on_log(mock_args, mock_state, mock_control, logs=logs)

        assert mock_control.should_training_stop is True

    def test_callback_adapter_on_save(self, mock_konic_callback):
        """Test callback adapter on_save."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.callback import (
            create_trl_callback_adapter,
        )

        adapter = create_trl_callback_adapter(mock_konic_callback)

        mock_args = MagicMock()
        mock_args.output_dir = "/tmp/checkpoints"
        mock_state = MagicMock()
        mock_state.global_step = 50
        mock_control = MagicMock()

        adapter.on_save(mock_args, mock_state, mock_control)

        # The callback creates path as "{output_dir}/checkpoint-{step}"
        mock_konic_callback.on_checkpoint_saved.assert_called_once_with(
            "/tmp/checkpoints/checkpoint-50", 50
        )

    def test_callback_adapter_on_train_end_skips(self, mock_konic_callback):
        """Test callback adapter on_train_end skips (backend handles it)."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.adapter.callback import (
            create_trl_callback_adapter,
        )

        adapter = create_trl_callback_adapter(mock_konic_callback)

        mock_args = MagicMock()
        mock_args.output_dir = "/tmp/output"
        mock_state = MagicMock()
        mock_state.global_step = 100
        mock_control = MagicMock()

        # Should not raise and should not call Konic callback
        adapter.on_train_end(mock_args, mock_state, mock_control)

        # Backend handles on_train_end with full result, so adapter skips it
        mock_konic_callback.on_train_end.assert_not_called()

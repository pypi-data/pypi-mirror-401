"""Tests for konic.finetuning.config module."""

import pytest

from konic.common.errors import KonicValidationError
from konic.finetuning.config import (
    GenerationConfig,
    KonicFinetuningMethodType,
    LoraConfig,
    TrainingConfig,
)


class TestKonicFinetuningMethodType:
    """Tests for KonicFinetuningMethodType enum."""

    def test_native_ppo_value(self):
        assert KonicFinetuningMethodType.NATIVE_PPO.value == "NATIVE_PPO"

    def test_enum_is_string_subclass(self):
        assert isinstance(KonicFinetuningMethodType.NATIVE_PPO, str)


class TestLoraConfig:
    """Tests for LoraConfig dataclass."""

    def test_default_values(self):
        config = LoraConfig()
        assert config.r == 16
        assert config.lora_alpha == 32
        assert config.lora_dropout == 0.05
        assert config.target_modules == ["q_proj", "v_proj"]
        assert config.bias == "none"
        assert config.task_type == "CAUSAL_LM"
        assert config.fan_in_fan_out is False

    def test_custom_values(self):
        config = LoraConfig(
            r=8,
            lora_alpha=16,
            lora_dropout=0.1,
            target_modules=["k_proj", "o_proj"],
            bias="all",
            task_type="SEQ_CLS",
            fan_in_fan_out=True,
        )
        assert config.r == 8
        assert config.lora_alpha == 16
        assert config.lora_dropout == 0.1
        assert config.target_modules == ["k_proj", "o_proj"]
        assert config.bias == "all"
        assert config.task_type == "SEQ_CLS"
        assert config.fan_in_fan_out is True

    def test_to_dict(self):
        config = LoraConfig(r=8, lora_alpha=16)
        result = config.to_dict()
        assert result["r"] == 8
        assert result["lora_alpha"] == 16
        assert result["lora_dropout"] == 0.05
        assert result["target_modules"] == ["q_proj", "v_proj"]
        assert result["bias"] == "none"
        assert result["task_type"] == "CAUSAL_LM"

    def test_to_peft_config(self):
        pytest.importorskip("peft")
        config = LoraConfig(r=8)
        peft_config = config.to_peft_config()
        assert peft_config.r == 8


class TestTrainingConfig:
    """Tests for TrainingConfig dataclass."""

    def test_default_values(self):
        config = TrainingConfig()
        assert config.learning_rate == 1e-5
        assert config.samples_per_iteration == 1
        assert config.batch_size == 8
        assert config.gradient_accumulation_steps == 4
        assert config.max_grad_norm == 1.0
        assert config.kl_penalty_weight == 0.1
        assert config.clip_ratio == 0.2
        assert config.vf_coef == 0.5
        assert config.entropy_coef == 0.01
        assert config.gamma == 1.0
        assert config.gae_lambda == 0.95
        assert config.ppo_epochs == 4
        assert config.warmup_steps == 100
        assert config.weight_decay == 0.01

    def test_custom_values(self):
        config = TrainingConfig(
            learning_rate=5e-5,
            batch_size=16,
            ppo_epochs=8,
        )
        assert config.learning_rate == 5e-5
        assert config.batch_size == 16
        assert config.ppo_epochs == 8

    def test_validation_negative_learning_rate_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(learning_rate=-0.001)
        assert "learning_rate must be positive" in str(exc_info.value)

    def test_validation_zero_learning_rate_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(learning_rate=0)
        assert "learning_rate must be positive" in str(exc_info.value)

    def test_validation_gamma_out_of_range_low_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(gamma=-0.1)
        assert "gamma must be in range [0, 1]" in str(exc_info.value)

    def test_validation_gamma_out_of_range_high_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(gamma=1.5)
        assert "gamma must be in range [0, 1]" in str(exc_info.value)

    def test_validation_gae_lambda_out_of_range_low_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(gae_lambda=-0.1)
        assert "gae_lambda must be in range [0, 1]" in str(exc_info.value)

    def test_validation_gae_lambda_out_of_range_high_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(gae_lambda=1.1)
        assert "gae_lambda must be in range [0, 1]" in str(exc_info.value)

    def test_validation_negative_clip_ratio_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(clip_ratio=-0.1)
        assert "clip_ratio must be positive" in str(exc_info.value)

    def test_validation_zero_clip_ratio_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            TrainingConfig(clip_ratio=0)
        assert "clip_ratio must be positive" in str(exc_info.value)

    def test_valid_boundary_values(self):
        config = TrainingConfig(gamma=0, gae_lambda=0)
        assert config.gamma == 0
        assert config.gae_lambda == 0

        config = TrainingConfig(gamma=1.0, gae_lambda=1.0)
        assert config.gamma == 1.0
        assert config.gae_lambda == 1.0

    def test_effective_batch_size(self):
        config = TrainingConfig(batch_size=4, gradient_accumulation_steps=8)
        assert config.effective_batch_size == 32

    def test_to_dict(self):
        config = TrainingConfig()
        result = config.to_dict()
        assert result["learning_rate"] == 1e-5
        assert result["batch_size"] == 8
        assert result["gradient_accumulation_steps"] == 4
        assert result["kl_penalty_weight"] == 0.1
        assert result["clip_ratio"] == 0.2

    def test_fast_debug_factory(self):
        config = TrainingConfig.fast_debug()
        assert config.learning_rate == 1e-4
        assert config.batch_size == 2
        assert config.gradient_accumulation_steps == 1
        assert config.ppo_epochs == 1
        assert config.warmup_steps == 0
        assert config.kl_penalty_weight == 0.0

    def test_cpu_optimized_factory(self):
        config = TrainingConfig.cpu_optimized()
        assert config.learning_rate == 5e-5
        assert config.batch_size == 1
        assert config.gradient_accumulation_steps == 8
        assert config.ppo_epochs == 2
        assert config.max_grad_norm == 0.5

    def test_gpu_optimized_factory(self):
        config = TrainingConfig.gpu_optimized()
        assert config.learning_rate == 1e-5
        assert config.batch_size == 16
        assert config.gradient_accumulation_steps == 2
        assert config.ppo_epochs == 4
        assert config.kl_penalty_weight == 0.1
        assert config.entropy_coef == 0.01


class TestGenerationConfig:
    """Tests for GenerationConfig dataclass."""

    def test_default_values(self):
        config = GenerationConfig()
        assert config.max_new_tokens == 128
        assert config.min_new_tokens == 1
        assert config.max_length == 512
        assert config.temperature == 1.0
        assert config.top_p == 1.0
        assert config.top_k == 0
        assert config.do_sample is True
        assert config.repetition_penalty == 1.0
        assert config.pad_token_id is None
        assert config.eos_token_id is None

    def test_custom_values(self):
        config = GenerationConfig(
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            do_sample=False,
        )
        assert config.max_new_tokens == 256
        assert config.temperature == 0.7
        assert config.top_p == 0.9
        assert config.top_k == 50
        assert config.do_sample is False

    def test_to_dict_basic(self):
        config = GenerationConfig()
        result = config.to_dict()
        assert result["max_new_tokens"] == 128
        assert result["min_new_tokens"] == 1
        assert result["temperature"] == 1.0
        assert result["top_p"] == 1.0
        assert result["do_sample"] is True
        assert result["repetition_penalty"] == 1.0
        assert "top_k" not in result  # top_k=0 excluded

    def test_to_dict_with_top_k(self):
        config = GenerationConfig(top_k=50)
        result = config.to_dict()
        assert result["top_k"] == 50

    def test_to_dict_with_pad_token_id(self):
        config = GenerationConfig(pad_token_id=0)
        result = config.to_dict()
        assert result["pad_token_id"] == 0

    def test_to_dict_with_eos_token_id(self):
        config = GenerationConfig(eos_token_id=2)
        result = config.to_dict()
        assert result["eos_token_id"] == 2

    def test_to_dict_with_eos_token_id_list(self):
        config = GenerationConfig(eos_token_id=[2, 3])
        result = config.to_dict()
        assert result["eos_token_id"] == [2, 3]

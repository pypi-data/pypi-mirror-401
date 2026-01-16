# pyright: reportArgumentType=false
"""Tests for konic.finetuning.module module."""

from unittest.mock import MagicMock, patch

import pytest
import torch
import torch.nn as nn

from konic.finetuning.config import KonicFinetuningMethodType
from konic.finetuning.module import (
    VALUE_HEAD_INIT_STD,
    BaseKonicLLMModule,
    KonicTorchRLHF,
    ValueHead,
    apply_lora,
    count_trainable_parameters,
    get_lora_state_dict,
    get_target_modules_for_model,
)


class TestValueHead:
    """Tests for ValueHead class."""

    def test_init(self):
        head = ValueHead(hidden_size=768)

        assert head.hidden_size == 768
        assert isinstance(head.dropout, nn.Dropout)
        assert isinstance(head.layers, nn.Sequential)

    def test_init_custom_dropout(self):
        head = ValueHead(hidden_size=512, dropout=0.2)
        assert head.dropout.p == 0.2

    def test_layers_structure(self):
        head = ValueHead(hidden_size=768)

        assert len(head.layers) == 4
        assert isinstance(head.layers[0], nn.Linear)
        assert isinstance(head.layers[1], nn.GELU)
        assert isinstance(head.layers[2], nn.Dropout)
        assert isinstance(head.layers[3], nn.Linear)

        # Check dimensions
        assert head.layers[0].in_features == 768
        assert head.layers[0].out_features == 384
        assert head.layers[3].in_features == 384
        assert head.layers[3].out_features == 1

    def test_forward_without_attention_mask(self):
        head = ValueHead(hidden_size=256)
        hidden_states = torch.randn(2, 10, 256)  # batch=2, seq=10, hidden=256

        values = head.forward(hidden_states)

        assert values.shape == (2,)

    def test_forward_with_attention_mask(self):
        head = ValueHead(hidden_size=256)
        hidden_states = torch.randn(2, 10, 256)
        # Use long tensor for attention mask since it's used for indexing
        attention_mask = torch.ones(2, 10, dtype=torch.long)
        attention_mask[0, 5:] = 0  # First sequence ends at position 4
        attention_mask[1, 8:] = 0  # Second sequence ends at position 7

        values = head.forward(hidden_states, attention_mask)

        assert values.shape == (2,)

    def test_forward_all_tokens(self):
        head = ValueHead(hidden_size=256)
        hidden_states = torch.randn(2, 10, 256)

        values = head.forward_all_tokens(hidden_states)

        assert values.shape == (2, 10)

    def test_weight_initialization(self):
        head = ValueHead(hidden_size=256)

        for layer in head.layers:
            if isinstance(layer, nn.Linear):
                # Check weight initialization is approximately correct
                assert layer.weight.std().item() < VALUE_HEAD_INIT_STD * 3
                # Bias should be zeros
                if layer.bias is not None:
                    assert torch.allclose(layer.bias, torch.zeros_like(layer.bias))


class TestApplyLora:
    """Tests for apply_lora function."""

    def test_apply_lora(self):
        peft = pytest.importorskip("peft")
        from konic.finetuning.config import LoraConfig

        mock_model = MagicMock()
        lora_config = LoraConfig(r=8)

        with patch.object(peft, "get_peft_model") as mock_get_peft:
            mock_peft_model = MagicMock()
            mock_get_peft.return_value = mock_peft_model

            result = apply_lora(mock_model, lora_config)

            mock_get_peft.assert_called_once()
            assert result is mock_peft_model


class TestGetLoraStateDict:
    """Tests for get_lora_state_dict function."""

    def test_extracts_lora_params(self):
        mock_model = MagicMock()
        mock_model.named_parameters.return_value = [
            ("layer.lora_A.weight", torch.tensor([1.0])),
            ("layer.lora_B.weight", torch.tensor([2.0])),
            ("layer.regular.weight", torch.tensor([3.0])),
        ]

        result = get_lora_state_dict(mock_model)

        assert "layer.lora_A.weight" in result
        assert "layer.lora_B.weight" in result
        assert "layer.regular.weight" not in result


class TestCountTrainableParameters:
    """Tests for count_trainable_parameters function."""

    def test_count_all_trainable(self):
        model = nn.Sequential(
            nn.Linear(10, 20),
            nn.Linear(20, 10),
        )

        trainable, total, percentage = count_trainable_parameters(model)

        expected_total = 10 * 20 + 20 + 20 * 10 + 10  # weights + biases
        assert total == expected_total
        assert trainable == total
        assert percentage == 100.0

    def test_count_partial_trainable(self):
        model = nn.Sequential(
            nn.Linear(10, 20),
            nn.Linear(20, 10),
        )
        # Freeze first layer
        for param in model[0].parameters():
            param.requires_grad = False

        trainable, total, percentage = count_trainable_parameters(model)

        assert trainable < total
        assert percentage < 100.0

    def test_count_empty_model(self):
        model = nn.Sequential()

        trainable, total, percentage = count_trainable_parameters(model)

        assert trainable == 0
        assert total == 0
        assert percentage == 0


class TestGetTargetModulesForModel:
    """Tests for get_target_modules_for_model function."""

    def test_llama(self):
        result = get_target_modules_for_model("llama")
        assert result == ["q_proj", "v_proj", "k_proj", "o_proj"]

    def test_mistral(self):
        result = get_target_modules_for_model("mistral")
        assert result == ["q_proj", "v_proj", "k_proj", "o_proj"]

    def test_falcon(self):
        result = get_target_modules_for_model("falcon")
        assert result == ["query_key_value", "dense"]

    def test_gpt2(self):
        result = get_target_modules_for_model("gpt2")
        assert result == ["c_attn", "c_proj"]

    def test_gpt_neox(self):
        result = get_target_modules_for_model("gpt_neox")
        assert result == ["query_key_value", "dense"]

    def test_opt(self):
        result = get_target_modules_for_model("opt")
        assert result == ["q_proj", "v_proj", "k_proj", "out_proj"]

    def test_bloom(self):
        result = get_target_modules_for_model("bloom")
        assert result == ["query_key_value", "dense"]

    def test_phi(self):
        result = get_target_modules_for_model("phi")
        assert result == ["q_proj", "v_proj", "k_proj", "dense"]

    def test_unknown_model_returns_default(self):
        result = get_target_modules_for_model("unknown_model_xyz")
        assert result == ["q_proj", "v_proj"]

    def test_case_insensitive(self):
        result = get_target_modules_for_model("LLAMA")
        assert result == ["q_proj", "v_proj", "k_proj", "o_proj"]

    def test_partial_match(self):
        result = get_target_modules_for_model("meta-llama/Llama-2-7b-hf")
        assert result == ["q_proj", "v_proj", "k_proj", "o_proj"]


class TestBaseKonicLLMModule:
    """Tests for BaseKonicLLMModule abstract class."""

    def test_peft_model_default(self):
        class ConcreteModule(BaseKonicLLMModule):
            @property
            def base_model(self):
                return MagicMock()

            @property
            def ref_model(self):
                return None

            def generate(self, input_ids, attention_mask=None, **kwargs):
                return input_ids

            def get_log_probs(self, input_ids, attention_mask=None, labels=None):
                return torch.zeros(1)

            def get_ref_log_probs(self, input_ids, attention_mask=None, labels=None):
                return torch.zeros(1)

        module = ConcreteModule()
        assert module.peft_model is None

    def test_get_hidden_states(self):
        class ConcreteModule(BaseKonicLLMModule):
            @property
            def base_model(self):
                mock_model = MagicMock()
                mock_output = MagicMock()
                mock_output.hidden_states = [torch.zeros(1, 10, 256) for _ in range(12)]
                mock_model.return_value = mock_output
                return mock_model

            @property
            def ref_model(self):
                return None

            def generate(self, input_ids, attention_mask=None, **kwargs):
                return input_ids

            def get_log_probs(self, input_ids, attention_mask=None, labels=None):
                return torch.zeros(1)

            def get_ref_log_probs(self, input_ids, attention_mask=None, labels=None):
                return torch.zeros(1)

        module = ConcreteModule()
        input_ids = torch.randint(0, 100, (1, 10))

        hidden = module.get_hidden_states(input_ids)

        assert hidden.shape == (1, 10, 256)


class TestKonicTorchRLHF:
    """Tests for KonicTorchRLHF class."""

    def test_init_basic(self):
        module = KonicTorchRLHF(model_name="gpt2")

        assert module.model_name == "gpt2"
        assert module._lora_config is None
        assert module._models_loaded is False
        assert module.method == KonicFinetuningMethodType.NATIVE_PPO

    def test_init_with_lora(self):
        from konic.finetuning.config import LoraConfig

        lora = LoraConfig(r=8)
        module = KonicTorchRLHF(model_name="gpt2", lora_config=lora)

        assert module._lora_config is lora
        assert module._use_peft_for_ref is True

    def test_init_without_peft_ref(self):
        from konic.finetuning.config import LoraConfig

        lora = LoraConfig(r=8)
        module = KonicTorchRLHF(
            model_name="gpt2",
            lora_config=lora,
            use_peft_for_ref=False,
        )

        assert module._use_peft_for_ref is False

    def test_init_device_auto_cuda(self):
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=True),
            patch("torch.backends.mps.is_available", return_value=False),
        ):
            module = KonicTorchRLHF(model_name="gpt2")
            assert module._device == torch.device("cuda")

    def test_init_device_auto_mps(self):
        with patch("torch.cuda.is_available", return_value=False):
            with patch("torch.backends.mps.is_available", return_value=True):
                module = KonicTorchRLHF(model_name="gpt2")
                assert module._device == torch.device("mps")
                assert module._dtype == torch.float32

    def test_init_device_auto_cpu(self):
        with patch("torch.cuda.is_available", return_value=False):
            with patch("torch.backends.mps.is_available", return_value=False):
                module = KonicTorchRLHF(model_name="gpt2")
                assert module._device == torch.device("cpu")

    def test_init_custom_device(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        assert module._device == torch.device("cpu")

    def test_init_custom_dtype(self):
        module = KonicTorchRLHF(model_name="gpt2", dtype=torch.bfloat16)
        assert module._dtype == torch.bfloat16

    def test_uses_peft_reference_property(self):
        from konic.finetuning.config import LoraConfig

        module_without_lora = KonicTorchRLHF(model_name="gpt2")
        assert module_without_lora.uses_peft_reference is False

        module_with_lora = KonicTorchRLHF(
            model_name="gpt2",
            lora_config=LoraConfig(),
        )
        assert module_with_lora.uses_peft_reference is True

    def test_setup_already_loaded(self):
        module = KonicTorchRLHF(model_name="gpt2")
        module._models_loaded = True

        # Should return early without doing anything
        module.setup()

    def test_setup_loads_model_and_tokenizer(self):
        with (
            patch("transformers.AutoModelForCausalLM") as mock_model_cls,
            patch("transformers.AutoTokenizer") as mock_tokenizer_cls,
        ):
            mock_model = MagicMock()
            mock_model.config.hidden_size = 768
            mock_model.parameters.return_value = iter([torch.nn.Parameter(torch.zeros(1))])
            mock_model_cls.from_pretrained.return_value = mock_model

            mock_tokenizer = MagicMock()
            mock_tokenizer.pad_token = None
            mock_tokenizer.eos_token = "</s>"
            mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer

            module = KonicTorchRLHF(model_name="gpt2", device="cpu")
            module.setup()

            assert module._models_loaded is True
            mock_model_cls.from_pretrained.assert_called()
            mock_tokenizer_cls.from_pretrained.assert_called()

    def test_base_model_property_calls_setup(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        mock_model = MagicMock()
        module._base_model = mock_model
        module._models_loaded = True

        result = module.base_model

        assert result is mock_model

    def test_ref_model_property(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        mock_ref = MagicMock()
        module._ref_model = mock_ref
        module._models_loaded = True

        result = module.ref_model

        assert result is mock_ref

    def test_tokenizer_property(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        mock_tokenizer = MagicMock()
        module._tokenizer = mock_tokenizer
        module._models_loaded = True

        result = module.tokenizer

        assert result is mock_tokenizer

    def test_value_head_property(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        mock_value_head = MagicMock()
        module._value_head = mock_value_head
        module._models_loaded = True

        result = module.value_head

        assert result is mock_value_head

    def test_generate_calls_setup_if_needed(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_model.generate.return_value = torch.tensor([[1, 2, 3]])
        module._base_model = mock_model
        module._peft_model = None

        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token_id = 0
        module._tokenizer = mock_tokenizer

        module._models_loaded = True

        module.generate(torch.tensor([[1, 2]]))

        mock_model.generate.assert_called_once()

    def test_generate_with_generation_config(self):
        from konic.finetuning.config import GenerationConfig

        gen_config = GenerationConfig(
            max_new_tokens=64,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
        )

        module = KonicTorchRLHF(
            model_name="gpt2",
            generation_config=gen_config,
            device="cpu",
        )

        mock_model = MagicMock()
        mock_model.generate.return_value = torch.tensor([[1, 2, 3]])
        module._base_model = mock_model
        module._peft_model = None

        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token_id = 0
        module._tokenizer = mock_tokenizer

        module._models_loaded = True

        module.generate(torch.tensor([[1, 2]]))

        call_kwargs = mock_model.generate.call_args.kwargs
        assert call_kwargs["max_new_tokens"] == 64
        assert call_kwargs["temperature"] == 0.7

    def test_get_log_probs(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        # logits shape: [batch, seq, vocab]
        mock_output.logits = torch.randn(2, 10, 100)
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None
        module._models_loaded = True

        input_ids = torch.randint(0, 100, (2, 10))
        log_probs = module.get_log_probs(input_ids)

        assert log_probs.shape == (2, 9)  # seq_len - 1

    def test_get_ref_log_probs_with_separate_model(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        module._use_peft_for_ref = False

        mock_ref = MagicMock()
        mock_output = MagicMock()
        mock_output.logits = torch.randn(2, 10, 100)
        mock_ref.return_value = mock_output
        module._ref_model = mock_ref
        module._peft_model = None
        module._models_loaded = True

        input_ids = torch.randint(0, 100, (2, 10))
        log_probs = module.get_ref_log_probs(input_ids)

        assert log_probs.shape == (2, 9)
        mock_ref.assert_called()

    def test_get_ref_log_probs_with_peft_disabled(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        module._use_peft_for_ref = True

        mock_peft = MagicMock()
        mock_output = MagicMock()
        mock_output.logits = torch.randn(2, 10, 100)
        mock_peft.return_value = mock_output
        mock_peft.disable_adapter.return_value.__enter__ = MagicMock()
        mock_peft.disable_adapter.return_value.__exit__ = MagicMock()
        module._peft_model = mock_peft
        module._models_loaded = True

        input_ids = torch.randint(0, 100, (2, 10))
        log_probs = module.get_ref_log_probs(input_ids)

        assert log_probs.shape == (2, 9)
        mock_peft.disable_adapter.assert_called()

    def test_compute_values(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.hidden_states = [torch.randn(2, 10, 256) for _ in range(12)]
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None

        mock_value_head = MagicMock()
        mock_value_head.return_value = torch.randn(2)
        module._value_head = mock_value_head

        module._models_loaded = True

        input_ids = torch.randint(0, 100, (2, 10))
        module.compute_values(input_ids)

        mock_value_head.assert_called_once()

    def test_compute_values_for_all_tokens(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.hidden_states = [torch.randn(2, 10, 256) for _ in range(12)]
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None

        mock_value_head = MagicMock()
        mock_value_head.forward_all_tokens.return_value = torch.randn(2, 10)
        module._value_head = mock_value_head

        module._models_loaded = True

        input_ids = torch.randint(0, 100, (2, 10))
        module.compute_values_for_all_tokens(input_ids)

        mock_value_head.forward_all_tokens.assert_called_once()

    def test_forward_with_cache(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.hidden_states = [torch.randn(2, 10, 256) for _ in range(12)]
        mock_output.logits = torch.randn(2, 10, 100)
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None

        mock_value_head = ValueHead(hidden_size=256)
        module._value_head = mock_value_head

        module._models_loaded = True

        input_ids = torch.randint(0, 100, (2, 10))
        log_probs, values, hidden = module.forward_with_cache(input_ids)

        assert log_probs.shape == (2, 9)
        assert values.shape == (2, 10)
        assert hidden.shape == (2, 10, 256)

    def test_get_trainable_parameters_with_peft(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        # Mock PEFT model with trainable params
        mock_peft = MagicMock()
        trainable_param = torch.nn.Parameter(torch.zeros(10))
        trainable_param.requires_grad = True
        frozen_param = torch.nn.Parameter(torch.zeros(10))
        frozen_param.requires_grad = False
        mock_peft.parameters.return_value = iter([trainable_param, frozen_param])
        module._peft_model = mock_peft

        # Value head params
        value_head = ValueHead(hidden_size=256)
        module._value_head = value_head

        module._models_loaded = True

        params = module.get_trainable_parameters()

        # Should include trainable PEFT param + all value head params
        assert len(params) > 1
        assert trainable_param in params

    def test_get_trainable_parameters_without_peft(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        module._peft_model = None

        mock_base = MagicMock()
        param = torch.nn.Parameter(torch.zeros(10))
        param.requires_grad = True
        mock_base.parameters.return_value = iter([param])
        module._base_model = mock_base

        value_head = ValueHead(hidden_size=256)
        module._value_head = value_head

        module._models_loaded = True

        params = module.get_trainable_parameters()

        assert param in params

    def test_create_attention_mask(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token_id = 0
        module._tokenizer = mock_tokenizer
        module._models_loaded = True

        input_ids = torch.tensor([[1, 2, 0, 0], [1, 2, 3, 0]])
        mask = module._create_attention_mask(input_ids)

        expected = torch.tensor([[1, 1, 0, 0], [1, 1, 1, 0]])
        assert torch.equal(mask, expected)

    def test_save_pretrained(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_base = MagicMock()
        mock_tokenizer = MagicMock()
        mock_value_head = MagicMock()
        mock_value_head.state_dict.return_value = {}

        module._base_model = mock_base
        module._tokenizer = mock_tokenizer
        module._value_head = mock_value_head
        module._peft_model = None
        module._models_loaded = True

        with patch("os.makedirs"):
            with patch("torch.save"):
                module.save_pretrained("/tmp/test_save")

        mock_base.save_pretrained.assert_called_once_with("/tmp/test_save")
        mock_tokenizer.save_pretrained.assert_called_once_with("/tmp/test_save")

    def test_save_pretrained_with_peft(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_peft = MagicMock()
        mock_tokenizer = MagicMock()
        mock_value_head = MagicMock()
        mock_value_head.state_dict.return_value = {}

        module._peft_model = mock_peft
        module._tokenizer = mock_tokenizer
        module._value_head = mock_value_head
        module._models_loaded = True

        with patch("os.makedirs"):
            with patch("torch.save"):
                module.save_pretrained("/tmp/test_save")

        mock_peft.save_pretrained.assert_called_once_with("/tmp/test_save")


class TestFlashAttention:
    """Tests for Flash Attention support."""

    def test_flash_attention_enabled_by_default(self):
        module = KonicTorchRLHF(model_name="gpt2")
        assert module._use_flash_attention is True

    def test_flash_attention_disabled_explicitly(self):
        module = KonicTorchRLHF(model_name="gpt2", use_flash_attention=False)
        assert module._use_flash_attention is False

    def test_flash_attention_parameter_preserved_on_cpu(self):
        """Flash attention setting is preserved even on non-CUDA devices."""
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        assert module._use_flash_attention is True

    def test_flash_attention_disabled_uses_default_attention(self):
        """Test that disabling flash attention uses default attention implementation."""
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=True),
            patch("torch.backends.mps.is_available", return_value=False),
            patch("transformers.AutoModelForCausalLM") as mock_model_cls,
            patch("transformers.AutoTokenizer") as mock_tokenizer_cls,
            patch.object(ValueHead, "to"),  # Prevent CUDA device move
        ):
            mock_model = MagicMock()
            mock_model.config.hidden_size = 768
            mock_model_cls.from_pretrained.return_value = mock_model

            mock_tokenizer = MagicMock()
            mock_tokenizer.pad_token = "</s>"
            mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer

            # Disable flash attention explicitly
            module = KonicTorchRLHF(model_name="gpt2", use_flash_attention=False)
            module.setup()

            # Verify model was loaded without flash_attention_2
            call_kwargs = mock_model_cls.from_pretrained.call_args.kwargs
            assert call_kwargs.get("attn_implementation") is None


class TestAMPSupport:
    """Tests for Automatic Mixed Precision support."""

    def test_amp_enabled_on_cuda(self):
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=True),
        ):
            module = KonicTorchRLHF(model_name="gpt2")
            assert module._use_amp is True

    def test_amp_disabled_on_cpu(self):
        with patch("torch.cuda.is_available", return_value=False):
            module = KonicTorchRLHF(model_name="gpt2", use_amp=True)
            assert module._use_amp is False

    def test_amp_disabled_explicitly(self):
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=True),
        ):
            module = KonicTorchRLHF(model_name="gpt2", use_amp=False)
            assert module._use_amp is False

    def test_scaler_none_when_amp_disabled(self):
        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        module._use_amp = False
        module._scaler = None
        module._models_loaded = True

        assert module.scaler is None

    def test_use_amp_property(self):
        with patch("torch.cuda.is_available", return_value=False):
            module = KonicTorchRLHF(model_name="gpt2")
            assert module.use_amp is False

    def test_amp_dtype_cached_bfloat16(self):
        """Test amp_dtype is cached at init and uses bfloat16 when supported."""
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=True),
        ):
            module = KonicTorchRLHF(model_name="gpt2")
            assert module.amp_dtype == torch.bfloat16

    def test_amp_dtype_cached_float16_fallback(self):
        """Test amp_dtype falls back to float16 when bfloat16 not supported."""
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=False),
        ):
            module = KonicTorchRLHF(model_name="gpt2")
            assert module.amp_dtype == torch.float16

    def test_amp_dtype_float16_when_no_cuda(self):
        """Test amp_dtype is float16 when CUDA not available."""
        with patch("torch.cuda.is_available", return_value=False):
            module = KonicTorchRLHF(model_name="gpt2")
            assert module.amp_dtype == torch.float16

    def test_get_amp_context_returns_autocast_when_enabled(self):
        """Test get_amp_context returns autocast when AMP is enabled."""
        with (
            patch("torch.cuda.is_available", return_value=True),
            patch("torch.cuda.is_bf16_supported", return_value=True),
        ):
            module = KonicTorchRLHF(model_name="gpt2")
            module._use_amp = True
            context = module.get_amp_context()
            # Should be an autocast context
            assert hasattr(context, "__enter__")
            assert hasattr(context, "__exit__")

    def test_get_amp_context_returns_nullcontext_when_disabled(self):
        """Test get_amp_context returns nullcontext when AMP is disabled."""
        import contextlib

        module = KonicTorchRLHF(model_name="gpt2", device="cpu")
        module._use_amp = False
        context = module.get_amp_context()
        # Should be a nullcontext
        assert isinstance(context, contextlib.nullcontext)


class TestForwardAll:
    """Tests for the unified forward_all method."""

    def test_forward_all_returns_dataclass(self):
        from konic.finetuning.module import ForwardAllOutput

        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.hidden_states = [torch.randn(2, 10, 256) for _ in range(12)]
        mock_output.logits = torch.randn(2, 10, 100)
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None

        mock_value_head = ValueHead(hidden_size=256)
        module._value_head = mock_value_head
        module._models_loaded = True
        module._use_amp = False

        module.get_ref_log_probs = MagicMock(return_value=torch.zeros(2, 9))

        input_ids = torch.randint(0, 100, (2, 10))
        result = module.forward_all(input_ids)

        assert isinstance(result, ForwardAllOutput)
        assert result.log_probs.shape == (2, 9)
        assert result.values.shape == (2, 10)
        assert result.ref_log_probs.shape == (2, 9)
        assert result.hidden_states.shape == (2, 10, 256)

    def test_forward_all_without_ref_computation(self):
        from konic.finetuning.module import ForwardAllOutput

        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.hidden_states = [torch.randn(2, 10, 256) for _ in range(12)]
        mock_output.logits = torch.randn(2, 10, 100)
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None

        mock_value_head = ValueHead(hidden_size=256)
        module._value_head = mock_value_head
        module._models_loaded = True
        module._use_amp = False

        input_ids = torch.randint(0, 100, (2, 10))
        result = module.forward_all(input_ids, compute_ref=False)

        assert isinstance(result, ForwardAllOutput)
        assert torch.all(result.ref_log_probs == 0)

    def test_forward_all_with_attention_mask(self):
        from konic.finetuning.module import ForwardAllOutput

        module = KonicTorchRLHF(model_name="gpt2", device="cpu")

        mock_model = MagicMock()
        mock_output = MagicMock()
        mock_output.hidden_states = [torch.randn(2, 10, 256) for _ in range(12)]
        mock_output.logits = torch.randn(2, 10, 100)
        mock_model.return_value = mock_output
        module._base_model = mock_model
        module._peft_model = None

        mock_value_head = ValueHead(hidden_size=256)
        module._value_head = mock_value_head
        module._models_loaded = True
        module._use_amp = False

        module.get_ref_log_probs = MagicMock(return_value=torch.zeros(2, 9))

        input_ids = torch.randint(0, 100, (2, 10))
        attention_mask = torch.ones(2, 10)
        result = module.forward_all(input_ids, attention_mask=attention_mask)

        assert isinstance(result, ForwardAllOutput)
        mock_model.assert_called_once()

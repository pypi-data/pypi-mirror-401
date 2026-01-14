"""LLM finetuning modules for RLHF training with LoRA support."""

from __future__ import annotations

import contextlib
import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa: N812

from konic.finetuning.config import KonicFinetuningMethodType

if TYPE_CHECKING:
    from peft import PeftModel
    from transformers import PreTrainedModel, PreTrainedTokenizer

    from konic.finetuning.config import GenerationConfig, LoraConfig


VALUE_HEAD_INIT_STD = 0.02  # GPT-2-style init for stable training

logger = logging.getLogger(__name__)


@dataclass
class ForwardAllOutput:
    """Container for unified forward pass outputs."""

    log_probs: torch.Tensor
    values: torch.Tensor
    ref_log_probs: torch.Tensor
    hidden_states: torch.Tensor


class ValueHead(nn.Module):
    def __init__(self, hidden_size: int, dropout: float = 0.1):
        super().__init__()

        self.hidden_size = hidden_size
        self.dropout = nn.Dropout(dropout)

        # Two-layer MLP for value estimation
        # GELU activation chosen over Tanh for smoother gradients and better optimization
        # dynamics in deep networks (matches modern transformer architectures like GPT-2+)
        self.layers = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 1),
        )

        # Initialize weights
        self._init_weights()

    def _init_weights(self) -> None:
        for module in self.layers:
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=VALUE_HEAD_INIT_STD)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)

    def forward(
        self, hidden_states: torch.Tensor, attention_mask: torch.Tensor | None = None
    ) -> torch.Tensor:
        if attention_mask is not None:
            seq_lengths = attention_mask.sum(dim=1) - 1
            batch_indices = torch.arange(hidden_states.size(0), device=hidden_states.device)
            last_hidden = hidden_states[batch_indices, seq_lengths]
        else:
            last_hidden = hidden_states[:, -1, :]
        return self.layers(last_hidden).squeeze(-1)

    def forward_all_tokens(self, hidden_states: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = hidden_states.shape
        flat_hidden = hidden_states.view(-1, self.hidden_size)
        flat_values = self.layers(flat_hidden)
        return flat_values.view(batch_size, seq_len)


def apply_lora(model: PreTrainedModel, lora_config: LoraConfig) -> PeftModel:
    from peft import get_peft_model

    peft_config = lora_config.to_peft_config()
    peft_model = get_peft_model(model, peft_config)

    return peft_model  # type: ignore[return-value]


def get_lora_state_dict(model: PeftModel) -> dict:
    state_dict = {}
    for name, param in model.named_parameters():
        if "lora_" in name:
            state_dict[name] = param.data.clone()
    return state_dict


def count_trainable_parameters(model: PreTrainedModel) -> tuple[int, int, float]:
    trainable_params = 0
    total_params = 0
    for param in model.parameters():
        total_params += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    percentage = 100 * trainable_params / total_params if total_params > 0 else 0
    return trainable_params, total_params, percentage


def get_target_modules_for_model(model_type: str) -> list[str]:
    target_modules_map = {
        "llama": ["q_proj", "v_proj", "k_proj", "o_proj"],
        "mistral": ["q_proj", "v_proj", "k_proj", "o_proj"],
        "falcon": ["query_key_value", "dense"],
        "gpt2": ["c_attn", "c_proj"],
        "gpt_neox": ["query_key_value", "dense"],
        "opt": ["q_proj", "v_proj", "k_proj", "out_proj"],
        "bloom": ["query_key_value", "dense"],
        "phi": ["q_proj", "v_proj", "k_proj", "dense"],
    }

    model_type_lower = model_type.lower()
    for key, modules in target_modules_map.items():
        if key in model_type_lower:
            return modules
    return ["q_proj", "v_proj"]  # Default for transformer models


class BaseKonicLLMModule(nn.Module, ABC):
    method: KonicFinetuningMethodType

    @property
    @abstractmethod
    def base_model(self) -> PreTrainedModel:
        pass

    @property
    @abstractmethod
    def ref_model(self) -> PreTrainedModel | None:
        pass

    @property
    def peft_model(self) -> PeftModel | None:
        return None

    @abstractmethod
    def generate(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor | None = None, **kwargs
    ) -> torch.Tensor:
        pass

    @abstractmethod
    def get_log_probs(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        labels: torch.Tensor | None = None,
    ) -> torch.Tensor:
        pass

    @abstractmethod
    def get_ref_log_probs(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        labels: torch.Tensor | None = None,
    ) -> torch.Tensor:
        pass

    def get_hidden_states(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor | None = None
    ) -> torch.Tensor:
        outputs = self.base_model(
            input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        return outputs.hidden_states[-1]


class KonicTorchRLHF(BaseKonicLLMModule):
    method = KonicFinetuningMethodType.NATIVE_PPO

    def __init__(
        self,
        model_name: str,
        tokenizer: PreTrainedTokenizer | None = None,
        lora_config: LoraConfig | None = None,
        generation_config: GenerationConfig | None = None,
        device: str | torch.device | None = None,
        dtype: torch.dtype | None = None,
        trust_remote_code: bool = False,
        use_peft_for_ref: bool = True,
        use_flash_attention: bool = True,
        use_amp: bool = True,
    ):
        self._models_loaded = False
        self._setup_lock = threading.Lock()

        self.model_name = model_name
        self._lora_config = lora_config
        self._generation_config = generation_config
        self._trust_remote_code = trust_remote_code
        self._tokenizer = tokenizer

        # PEFT weight sharing: only enabled if using LoRA
        self._use_peft_for_ref = use_peft_for_ref and (lora_config is not None)

        # Flash Attention and AMP settings
        self._use_flash_attention = use_flash_attention
        if use_amp and not torch.cuda.is_available():
            logger.warning("AMP requested but CUDA not available, disabling AMP")
        self._use_amp = use_amp and torch.cuda.is_available()
        self._scaler: torch.cuda.amp.GradScaler | None = None

        # Cache bfloat16 support check (avoids repeated CUDA queries during forward passes)
        self._amp_dtype: torch.dtype = torch.float16
        if torch.cuda.is_available():
            try:
                if torch.cuda.is_bf16_supported():
                    self._amp_dtype = torch.bfloat16
            except (AssertionError, RuntimeError):
                pass  # CUDA not initialized, use float16 default

        # Determine device
        if device is None:
            if torch.cuda.is_available():
                self._device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self._device = torch.device("mps")
            else:
                self._device = torch.device("cpu")
        else:
            self._device = torch.device(device)

        # Determine dtype: float32 for MPS (numerical stability), float16 for CUDA
        if dtype is not None:
            self._dtype = dtype
        elif self._device.type == "mps":
            # MPS has numerical stability issues with float16 during generation
            self._dtype = torch.float32
            logger.info("Using float32 for MPS device (numerical stability)")
        elif self._device.type == "cuda":
            self._dtype = torch.float16
        else:
            self._dtype = torch.float32

        self._base_model: PreTrainedModel | None = None
        self._ref_model: PreTrainedModel | None = None
        self._peft_model: PeftModel | None = None
        self._value_head: ValueHead | None = None

        super().__init__()

    def setup(self) -> None:
        import warnings

        if self._models_loaded:
            return

        with self._setup_lock:
            if self._models_loaded:
                return

            from transformers import AutoModelForCausalLM, AutoTokenizer

            if self._trust_remote_code:
                warnings.warn(
                    f"Loading model '{self.model_name}' with trust_remote_code=True. "
                    "This executes arbitrary code from the model repository. "
                    "Only use this with models you trust.",
                    UserWarning,
                    stacklevel=2,
                )

            if self._tokenizer is None:
                self._tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name, trust_remote_code=self._trust_remote_code
                )
                if self._tokenizer.pad_token is None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token

            self._tokenizer.padding_side = "left"  # Required for decoder-only generation

            # Use Flash Attention 2 if available and requested
            attn_implementation = None
            if self._use_flash_attention and self._device.type == "cuda":
                try:
                    import flash_attn  # type: ignore[import-not-found]  # noqa: F401

                    attn_implementation = "flash_attention_2"
                    logger.info("Flash Attention 2 available, will attempt to use")
                except ImportError:
                    logger.warning(
                        "Flash Attention requested (use_flash_attention=True) but not installed. "
                        "Install with: pip install flash-attn --no-build-isolation"
                    )

            # Load model with appropriate device handling
            # MPS doesn't support device_map or Flash Attention, load to CPU then move
            if self._device.type == "mps":
                self._base_model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    dtype=self._dtype,
                    trust_remote_code=self._trust_remote_code,
                )
                self._base_model = self._base_model.to(self._device)  # type: ignore[arg-type]
            else:
                try:
                    self._base_model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        dtype=self._dtype,
                        trust_remote_code=self._trust_remote_code,
                        device_map=self._device if self._device.type != "cpu" else None,
                        attn_implementation=attn_implementation,
                    )
                except (ValueError, ImportError) as e:
                    # Flash Attention failures: ValueError (unsupported arch), ImportError (missing deps)
                    if attn_implementation is not None:
                        logger.warning(
                            f"Flash Attention initialization failed: {e}. "
                            "Falling back to default attention."
                        )
                        self._base_model = AutoModelForCausalLM.from_pretrained(
                            self.model_name,
                            dtype=self._dtype,
                            trust_remote_code=self._trust_remote_code,
                            device_map=self._device if self._device.type != "cpu" else None,
                        )
                    else:
                        raise

            if self._lora_config is not None:
                assert self._base_model is not None
                self._peft_model = apply_lora(self._base_model, self._lora_config)
                self._base_model = self._peft_model.get_base_model()  # type: ignore[assignment]

            if self._use_peft_for_ref:
                self._ref_model = None
                logger.info(
                    "Using PEFT weight sharing for reference model (~50%% memory reduction)"
                )
            else:
                # Load reference model with same device handling
                if self._device.type == "mps":
                    self._ref_model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        dtype=self._dtype,
                        trust_remote_code=self._trust_remote_code,
                    )
                    self._ref_model = self._ref_model.to(self._device)  # type: ignore[arg-type]
                else:
                    self._ref_model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        dtype=self._dtype,
                        trust_remote_code=self._trust_remote_code,
                        device_map=self._device if self._device.type != "cpu" else None,
                    )
                self._ref_model.requires_grad_(False)

            assert self._base_model is not None
            hidden_size = self._base_model.config.hidden_size
            self._value_head = ValueHead(hidden_size=hidden_size)
            self._value_head.to(device=self._device, dtype=self._dtype)

            # Initialize AMP GradScaler if enabled
            if self._use_amp:
                self._scaler = torch.cuda.amp.GradScaler()
                logger.info("AMP GradScaler initialized for mixed precision training")

            self._models_loaded = True

    @property
    def base_model(self) -> PreTrainedModel:
        if not self._models_loaded:
            self.setup()
        assert self._base_model is not None
        return self._base_model

    @property
    def ref_model(self) -> PreTrainedModel | None:
        if not self._models_loaded:
            self.setup()
        return self._ref_model

    @property
    def uses_peft_reference(self) -> bool:
        return self._use_peft_for_ref

    @property
    def peft_model(self) -> PeftModel | None:
        return self._peft_model

    @property
    def tokenizer(self) -> PreTrainedTokenizer:
        if not self._models_loaded:
            self.setup()
        assert self._tokenizer is not None
        return self._tokenizer

    @property
    def value_head(self) -> ValueHead:
        if not self._models_loaded:
            self.setup()
        assert self._value_head is not None
        return self._value_head

    @property
    def scaler(self) -> torch.cuda.amp.GradScaler | None:
        """AMP gradient scaler, None if AMP is disabled."""
        return self._scaler

    @property
    def use_amp(self) -> bool:
        """Whether automatic mixed precision is enabled."""
        return self._use_amp

    @property
    def amp_dtype(self) -> torch.dtype:
        """AMP dtype (bfloat16 if supported, else float16). Cached at init."""
        return self._amp_dtype

    def get_amp_context(self) -> contextlib.AbstractContextManager:
        """Return autocast context if AMP is enabled, else nullcontext."""
        if self._use_amp:
            return torch.cuda.amp.autocast(dtype=self._amp_dtype)
        return contextlib.nullcontext()

    def generate(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        **kwargs,
    ) -> torch.Tensor:
        if not self._models_loaded:
            self.setup()

        gen_kwargs = {}
        if self._generation_config is not None:
            gen_kwargs = {
                "max_new_tokens": self._generation_config.max_new_tokens,
                "temperature": self._generation_config.temperature,
                "top_p": self._generation_config.top_p,
                "top_k": self._generation_config.top_k,
                "do_sample": self._generation_config.do_sample,
                "repetition_penalty": self._generation_config.repetition_penalty,
            }
        gen_kwargs.update(kwargs)
        gen_kwargs["pad_token_id"] = self.tokenizer.pad_token_id
        gen_kwargs.setdefault("use_cache", True)
        gen_kwargs.setdefault("num_beams", 1)
        if not gen_kwargs.get("do_sample", True):
            gen_kwargs.setdefault("early_stopping", True)

        # Numerical stability: ensure temperature is reasonable for sampling
        if gen_kwargs.get("do_sample", True):
            temp = gen_kwargs.get("temperature", 1.0)
            # Clamp temperature to avoid numerical issues (too low = inf, too high = uniform)
            gen_kwargs["temperature"] = max(0.1, min(temp, 2.0))

        model: PreTrainedModel = (
            self._peft_model if self._peft_model is not None else self.base_model
        )  # type: ignore[assignment]

        # Ensure inputs are on the correct device
        input_ids = input_ids.to(self._device)
        if attention_mask is not None:
            attention_mask = attention_mask.to(self._device)

        with torch.inference_mode():
            outputs = model.generate(  # type: ignore[operator]
                input_ids=input_ids, attention_mask=attention_mask, **gen_kwargs
            )
        return outputs

    def get_log_probs(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        labels: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if not self._models_loaded:
            self.setup()

        model = self._peft_model if self._peft_model is not None else self.base_model

        outputs = model(
            input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=False
        )
        logits = outputs.logits
        shift_logits = logits[:, :-1, :]
        shift_labels = labels[:, 1:] if labels is not None else input_ids[:, 1:]
        log_probs = F.log_softmax(shift_logits, dim=-1)
        token_log_probs = log_probs.gather(dim=-1, index=shift_labels.unsqueeze(-1)).squeeze(-1)
        return token_log_probs

    def get_ref_log_probs(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        labels: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if not self._models_loaded:
            self.setup()

        with torch.no_grad():
            if self._use_peft_for_ref and self._peft_model is not None:
                with self._peft_model.disable_adapter():
                    outputs = self._peft_model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_hidden_states=False,
                    )
            else:
                assert self._ref_model is not None
                outputs = self._ref_model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    output_hidden_states=False,
                )

            logits = outputs.logits
            shift_logits = logits[:, :-1, :]
            shift_labels = labels[:, 1:] if labels is not None else input_ids[:, 1:]
            log_probs = F.log_softmax(shift_logits, dim=-1)
            token_log_probs = log_probs.gather(dim=-1, index=shift_labels.unsqueeze(-1)).squeeze(-1)

        return token_log_probs

    def compute_values(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor | None = None
    ) -> torch.Tensor:
        hidden_states = self.get_hidden_states(input_ids, attention_mask)
        return self.value_head(hidden_states, attention_mask)

    def compute_values_for_all_tokens(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor | None = None
    ) -> torch.Tensor:
        hidden_states = self.get_hidden_states(input_ids, attention_mask)
        return self.value_head.forward_all_tokens(hidden_states)

    def forward_with_cache(
        self, input_ids: torch.Tensor, attention_mask: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if not self._models_loaded:
            self.setup()

        model = self._peft_model if self._peft_model is not None else self.base_model

        outputs = model(
            input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True
        )
        hidden_states = outputs.hidden_states[-1]
        values = self.value_head.forward_all_tokens(hidden_states)

        logits = outputs.logits
        shift_logits = logits[:, :-1, :]
        shift_labels = input_ids[:, 1:]
        log_probs = F.log_softmax(shift_logits, dim=-1)
        token_log_probs = log_probs.gather(dim=-1, index=shift_labels.unsqueeze(-1)).squeeze(-1)

        return token_log_probs, values, hidden_states

    def forward_all(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        compute_ref: bool = True,
    ) -> ForwardAllOutput:
        """Unified forward pass for PPO training, computing all outputs in a single pass.

        Args:
            input_ids: Token IDs of shape (batch_size, seq_len).
            attention_mask: Optional attention mask of shape (batch_size, seq_len).
            compute_ref: If True, compute reference model log probs for KL penalty.

        Returns:
            ForwardAllOutput containing log_probs, values, ref_log_probs, hidden_states.
        """
        if not self._models_loaded:
            self.setup()

        model = self._peft_model if self._peft_model is not None else self.base_model

        with self.get_amp_context():
            # Active model forward with hidden states
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_hidden_states=True,
            )

            hidden_states = outputs.hidden_states[-1]
            values = self.value_head.forward_all_tokens(hidden_states)

            # Compute log probs
            logits = outputs.logits
            shift_logits = logits[:, :-1, :]
            shift_labels = input_ids[:, 1:]
            log_probs = F.log_softmax(shift_logits, dim=-1)
            token_log_probs = log_probs.gather(dim=-1, index=shift_labels.unsqueeze(-1)).squeeze(-1)

        # Reference log probs computed outside autocast context to ensure consistent
        # precision with frozen reference model weights (avoids mixed-precision drift
        # between policy and reference distributions during KL divergence computation)
        ref_log_probs = torch.zeros_like(token_log_probs)
        if compute_ref:
            with torch.no_grad():
                ref_log_probs = self.get_ref_log_probs(input_ids, attention_mask)

        return ForwardAllOutput(
            log_probs=token_log_probs,
            values=values,
            ref_log_probs=ref_log_probs,
            hidden_states=hidden_states,
        )

    def _create_attention_mask(self, input_ids: torch.Tensor) -> torch.Tensor:
        pad_token_id = self.tokenizer.pad_token_id
        return (input_ids != pad_token_id).long()  # type: ignore[union-attr]

    def get_trainable_parameters(self) -> list[torch.nn.Parameter]:
        params = []
        if self._peft_model is not None:
            for param in self._peft_model.parameters():
                if param.requires_grad:
                    params.append(param)
        else:
            for param in self.base_model.parameters():
                if param.requires_grad:
                    params.append(param)
        for param in self.value_head.parameters():
            params.append(param)
        return params

    def save_pretrained(self, save_path: str) -> None:
        import os

        os.makedirs(save_path, exist_ok=True)
        if self._peft_model is not None:
            self._peft_model.save_pretrained(save_path)
        else:
            self.base_model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)
        value_head_path = os.path.join(save_path, "value_head.pt")
        torch.save(self.value_head.state_dict(), value_head_path)

    def load_pretrained(self, load_path: str) -> None:
        import os

        if self._peft_model is not None:
            from peft import PeftModel

            self._peft_model = PeftModel.from_pretrained(self.base_model, load_path)
        else:
            from transformers import AutoModelForCausalLM

            if self._device.type == "mps":
                self._base_model = AutoModelForCausalLM.from_pretrained(
                    load_path, dtype=self._dtype
                )
                self._base_model = self._base_model.to(self._device)  # type: ignore[arg-type]
            else:
                self._base_model = AutoModelForCausalLM.from_pretrained(
                    load_path,
                    dtype=self._dtype,
                    device_map=self._device if self._device.type != "cpu" else None,
                )

        value_head_path = os.path.join(load_path, "value_head.pt")
        if os.path.exists(value_head_path):
            self.value_head.load_state_dict(torch.load(value_head_path, map_location=self._device))

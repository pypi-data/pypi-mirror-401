"""Reward composition and reduction for LLM finetuning."""

from __future__ import annotations

import functools
import gc
import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import TYPE_CHECKING

from konic.common.errors import KonicRuntimeError, KonicValidationError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import torch

    from konic.finetuning.environment import BaseKonicLLMEnvironment


class LLMRewardKeys(str, Enum):
    CUSTOM_REWARD_FN_ATTR_KEY = "_is_llm_reward_fn"


def llm_reward(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    setattr(wrapper, LLMRewardKeys.CUSTOM_REWARD_FN_ATTR_KEY.value, True)
    return wrapper


def get_llm_reward_fns(obj: object) -> list[Callable]:
    reward_fns = []

    for name in dir(obj):
        if name.startswith("_"):
            continue

        try:
            attr = getattr(obj, name)
        except AttributeError:
            continue

        if callable(attr) and hasattr(attr, LLMRewardKeys.CUSTOM_REWARD_FN_ATTR_KEY.value):
            if getattr(attr, LLMRewardKeys.CUSTOM_REWARD_FN_ATTR_KEY.value):
                reward_fns.append(attr)

    return reward_fns


class BaseRewardModel(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compute_reward(self, prompt: str, response: str, **kwargs) -> float:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class HuggingFaceRewardModel(BaseRewardModel):
    def __init__(
        self,
        model_id: str,
        device: str | None = "auto",
        dtype: torch.dtype | None = None,
        max_length: int = 512,
        label_index: int | None = None,
        normalize: bool = False,
        normalize_min: float = -1.0,
        normalize_max: float = 1.0,
    ):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self._model_id = model_id
        self._dtype = dtype if dtype is not None else torch.float16
        self._max_length = max_length
        self._label_index = label_index
        self._normalize = normalize
        self._normalize_min = normalize_min
        self._normalize_max = normalize_max

        # Load model and tokenizer
        self._model = AutoModelForSequenceClassification.from_pretrained(
            model_id,
            dtype=self._dtype,
            device_map=device if device != "auto" else None,
        )
        self._tokenizer = AutoTokenizer.from_pretrained(model_id)

        # Ensure pad token is set
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        # Handle device
        if device == "auto":
            self._device = next(self._model.parameters()).device
        else:
            self._device = torch.device(device) if device else torch.device("cpu")
            self._model = self._model.to(self._device)

        # Set model to inference mode (no gradients)
        self._model.requires_grad_(False)

        # Track running stats for normalization
        self._running_mean = 0.0
        self._running_var = 1.0
        self._n_samples = 0

    @property
    def name(self) -> str:
        return f"hf_{self._model_id.replace('/', '_').replace('-', '_')}"

    @property
    def model_id(self) -> str:
        return self._model_id

    def compute_reward(self, prompt: str, response: str, **kwargs) -> float:
        import torch

        # Combine prompt and response
        text = self._format_input(prompt, response)

        # Tokenize
        if self._tokenizer is None:
            raise KonicRuntimeError("Tokenizer not loaded", operation="compute_reward")
        inputs = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self._max_length,
            padding=True,
        ).to(self._device)

        # Get model output
        if self._model is None:
            raise KonicRuntimeError("Model not loaded", operation="compute_reward")
        with torch.no_grad():
            outputs = self._model(**inputs)

        # Extract reward from logits
        logits = outputs.logits

        if logits.shape[-1] == 1:
            # Single output - use directly
            reward = logits[0, 0].item()
        elif self._label_index is not None:
            # Use specified label index
            reward = logits[0, self._label_index].item()
        else:
            # Default: use first logit or mean
            reward = logits[0, 0].item()

        # Optional normalization
        if self._normalize:
            reward = self._normalize_reward(reward)

        return reward

    def _format_input(self, prompt: str, response: str) -> str:
        return f"{prompt}\n{response}"

    def _normalize_reward(self, reward: float) -> float:
        self._n_samples += 1
        delta = reward - self._running_mean
        self._running_mean += delta / self._n_samples
        delta2 = reward - self._running_mean
        self._running_var += (delta * delta2 - self._running_var) / self._n_samples

        # Normalize to standard normal
        std = max(self._running_var**0.5, 1e-8)
        normalized = (reward - self._running_mean) / std

        # Scale to target range
        range_size = self._normalize_max - self._normalize_min
        scaled = (normalized + 3) / 6  # Assume ~99.7% within 3 std
        scaled = max(0, min(1, scaled))  # Clamp to [0, 1]
        return self._normalize_min + scaled * range_size

    def batch_compute_reward(self, prompts: list[str], responses: list[str]) -> list[float]:
        import torch

        if len(prompts) != len(responses):
            raise KonicValidationError(
                f"prompts and responses must have same length "
                f"(got {len(prompts)} prompts, {len(responses)} responses)",
                field="prompts/responses",
            )

        # Format all inputs
        texts = [self._format_input(p, r) for p, r in zip(prompts, responses)]

        # Batch tokenize
        if self._tokenizer is None:
            raise KonicRuntimeError("Tokenizer not loaded", operation="batch_compute_reward")
        inputs = self._tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            max_length=self._max_length,
            padding=True,
        ).to(self._device)

        # Get model outputs
        if self._model is None:
            raise KonicRuntimeError("Model not loaded", operation="batch_compute_reward")
        with torch.no_grad():
            outputs = self._model(**inputs)

        logits = outputs.logits

        # Extract rewards
        if logits.shape[-1] == 1:
            rewards = logits[:, 0].tolist()
        elif self._label_index is not None:
            rewards = logits[:, self._label_index].tolist()
        else:
            rewards = logits[:, 0].tolist()

        # Optional normalization
        if self._normalize:
            rewards = [self._normalize_reward(r) for r in rewards]

        return rewards

    def cleanup(self) -> None:
        import torch

        if hasattr(self, "_model") and self._model is not None:
            # Move model to CPU first to free GPU memory, then delete
            self._model.cpu()
            del self._model
            self._model = None

        if hasattr(self, "_tokenizer") and self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None

        # Clear CUDA cache if available
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        gc.collect()

    def __del__(self) -> None:
        try:
            self.cleanup()
        except Exception:
            pass


class BaseRewardReducer(ABC):
    @abstractmethod
    def reduce(self, rewards: dict[str, float]) -> float:
        pass


class WeightedSumReducer(BaseRewardReducer):
    def __init__(self, weights: dict[str, float] | None = None, default_weight: float = 1.0):
        self._weights = weights or {}
        self._default_weight = default_weight

    def reduce(self, rewards: dict[str, float]) -> float:
        total = 0.0
        for name, value in rewards.items():
            weight = self._weights.get(name, self._default_weight)
            total += weight * value
        return total


class MeanReducer(BaseRewardReducer):
    def __init__(self, **kwargs) -> None:
        pass

    def reduce(self, rewards: dict[str, float]) -> float:
        if not rewards:
            return 0.0
        return sum(rewards.values()) / len(rewards)


class MaxReducer(BaseRewardReducer):
    def __init__(self, **kwargs) -> None:
        pass

    def reduce(self, rewards: dict[str, float]) -> float:
        if not rewards:
            return 0.0
        return max(rewards.values())


class BaseKonicLLMRewardComposer(ABC):
    _env: BaseKonicLLMEnvironment | None = None

    def set_env(self, env: BaseKonicLLMEnvironment) -> None:
        self._env = env

    @property
    def env(self) -> BaseKonicLLMEnvironment | None:
        return self._env

    @abstractmethod
    def compose(self, prompt: str, response: str) -> float:
        pass

    def compose_batch(
        self, prompts: list[str], responses: list[str]
    ) -> tuple[list[float], dict[str, list[float]]]:
        rewards = []
        breakdowns: dict[str, list[float]] = {}
        for prompt, response in zip(prompts, responses):
            reward = self.compose(prompt, response)
            rewards.append(reward)
        return rewards, breakdowns

    def get_reward_breakdown(self, prompt: str, response: str) -> dict[str, float]:
        return {}


class KonicLLMRewardComposer(BaseKonicLLMRewardComposer):
    reducer: type[BaseRewardReducer] = WeightedSumReducer

    def __init__(
        self,
        reward_models: list[BaseRewardModel] | None = None,
        reward_weights: dict[str, float] | None = None,
        kl_penalty_weight: float = 0.0,
        reducer: type[BaseRewardReducer] | None = None,
    ):
        super().__init__()

        self._reward_models = reward_models or []
        self._reward_weights = reward_weights or {}
        self._kl_penalty_weight = kl_penalty_weight

        if reducer is not None:
            self.reducer = reducer

    def add_reward_model(
        self, model: BaseRewardModel, weight: float = 1.0
    ) -> KonicLLMRewardComposer:
        self._reward_models.append(model)
        self._reward_weights[model.name] = weight
        return self

    def set_reward_weight(self, name: str, weight: float) -> KonicLLMRewardComposer:
        self._reward_weights[name] = weight
        return self

    @property
    def kl_penalty_weight(self) -> float:
        return self._kl_penalty_weight

    @kl_penalty_weight.setter
    def kl_penalty_weight(self, value: float) -> None:
        self._kl_penalty_weight = value

    def _compute_model_rewards_sequential(
        self,
        model: BaseRewardModel,
        prompts: list[str],
        responses: list[str],
        rewards_per_sample: list[dict[str, float]],
    ) -> None:
        """Compute rewards sequentially for a single model across all samples."""
        for i, (prompt, response) in enumerate(zip(prompts, responses)):
            try:
                rewards_per_sample[i][model.name] = model.compute_reward(prompt, response)
            except Exception:
                rewards_per_sample[i][model.name] = 0.0

    def compose(self, prompt: str, response: str) -> float:
        rewards: dict[str, float] = {}

        # Get rewards from registered models
        for model in self._reward_models:
            try:
                reward = model.compute_reward(prompt, response)
                rewards[model.name] = reward
            except Exception as e:
                # Log error but continue with other rewards
                logger.warning(f"Reward model {model.name} failed: {e}")
                rewards[model.name] = 0.0

        # Get rewards from @llm_reward decorated methods
        custom_fns = get_llm_reward_fns(self)
        for fn in custom_fns:
            try:
                result = fn(prompt, response)

                if isinstance(result, dict):
                    # Function returned multiple named rewards
                    rewards.update(result)
                elif isinstance(result, (int | float)):
                    # Function returned single reward
                    rewards[fn.__name__] = float(result)
            except Exception as e:
                logger.warning(f"Custom reward function {fn.__name__} failed: {e}")

        # Reduce rewards to single value
        reducer_instance = self.reducer(weights=self._reward_weights)  # type: ignore[call-arg]
        total_reward = reducer_instance.reduce(rewards)

        return total_reward

    def compose_batch(
        self, prompts: list[str], responses: list[str]
    ) -> tuple[list[float], dict[str, list[float]]]:
        if len(prompts) != len(responses):
            raise KonicValidationError(
                f"prompts and responses must have same length "
                f"(got {len(prompts)} prompts, {len(responses)} responses)",
                field="prompts/responses",
            )

        batch_size = len(prompts)
        rewards_per_sample: list[dict[str, float]] = [{} for _ in range(batch_size)]

        # OPTIMIZATION: Batch process HuggingFace reward models
        for model in self._reward_models:
            if isinstance(model, HuggingFaceRewardModel):
                try:
                    # Use batch computation - much faster than sequential
                    batch_rewards = model.batch_compute_reward(prompts, responses)
                    for i, reward in enumerate(batch_rewards):
                        rewards_per_sample[i][model.name] = reward
                except Exception as e:
                    logger.warning(
                        f"Batch reward computation failed for {model.name}, "
                        f"falling back to sequential: {e}"
                    )
                    self._compute_model_rewards_sequential(
                        model, prompts, responses, rewards_per_sample
                    )
            else:
                # Non-HuggingFace models: process sequentially
                self._compute_model_rewards_sequential(
                    model, prompts, responses, rewards_per_sample
                )

        # Process custom @llm_reward functions (always sequential)
        custom_fns = get_llm_reward_fns(self)
        for fn in custom_fns:
            for i, (prompt, response) in enumerate(zip(prompts, responses)):
                try:
                    result = fn(prompt, response)
                    if isinstance(result, dict):
                        rewards_per_sample[i].update(result)
                    elif isinstance(result, (int | float)):
                        rewards_per_sample[i][fn.__name__] = float(result)
                except Exception as e:
                    logger.warning(f"Custom reward {fn.__name__} failed: {e}")

        # Reduce to final rewards
        reducer_instance = self.reducer(weights=self._reward_weights)  # type: ignore[call-arg]
        final_rewards = [reducer_instance.reduce(r) for r in rewards_per_sample]

        # Build breakdown dict
        breakdowns: dict[str, list[float]] = {}
        for sample_rewards in rewards_per_sample:
            for key, value in sample_rewards.items():
                if key not in breakdowns:
                    breakdowns[key] = []
                breakdowns[key].append(value)

        logger.debug(f"Batch reward computation completed for {batch_size} samples")
        return final_rewards, breakdowns

    def compute_kl_penalty(
        self, log_probs: torch.Tensor, ref_log_probs: torch.Tensor
    ) -> torch.Tensor:
        kl_div = log_probs - ref_log_probs
        return self._kl_penalty_weight * kl_div

    def get_reward_breakdown(self, prompt: str, response: str) -> dict[str, float]:
        rewards: dict[str, float] = {}

        # Get rewards from registered models
        for model in self._reward_models:
            try:
                reward = model.compute_reward(prompt, response)
                rewards[model.name] = reward
            except Exception:
                rewards[model.name] = 0.0

        # Get rewards from @llm_reward decorated methods
        custom_fns = get_llm_reward_fns(self)
        for fn in custom_fns:
            try:
                result = fn(prompt, response)
                if isinstance(result, dict):
                    rewards.update(result)
                elif isinstance(result, (int | float)):
                    rewards[fn.__name__] = float(result)
            except Exception:
                pass

        return rewards

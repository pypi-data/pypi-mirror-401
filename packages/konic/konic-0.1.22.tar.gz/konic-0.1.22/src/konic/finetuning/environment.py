"""Environment classes for LLM finetuning."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

import gymnasium as gym
import numpy as np
import torch
from transformers import BatchEncoding, PreTrainedTokenizer, PreTrainedTokenizerFast

if TYPE_CHECKING:
    from transformers import PreTrainedModel

    from konic.finetuning.config import GenerationConfig
    from konic.finetuning.reward import BaseKonicLLMRewardComposer


class TokenizerWrapper:
    def __init__(self, tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast):
        self._tokenizer = tokenizer
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token
            self._tokenizer.pad_token_id = self._tokenizer.eos_token_id

    @property
    def tokenizer(self) -> PreTrainedTokenizer | PreTrainedTokenizerFast:
        return self._tokenizer

    @property
    def vocab_size(self) -> int:
        return self._tokenizer.vocab_size

    @property
    def pad_token(self) -> str:
        return cast(str, self._tokenizer.pad_token)

    @property
    def pad_token_id(self) -> int:
        return cast(int, self._tokenizer.pad_token_id)

    @property
    def eos_token(self) -> str:
        return cast(str, self._tokenizer.eos_token)

    @property
    def eos_token_id(self) -> int:
        return cast(int, self._tokenizer.eos_token_id)

    @property
    def bos_token(self) -> str | None:
        return cast(str | None, self._tokenizer.bos_token)

    @property
    def bos_token_id(self) -> int | None:
        return cast(int | None, self._tokenizer.bos_token_id)

    def encode(
        self,
        text: str,
        max_length: int | None = None,
        padding: bool | str = False,
        truncation: bool = True,
        return_tensors: str | None = None,
        add_special_tokens: bool = True,
    ) -> list[int] | torch.Tensor:
        result = self._tokenizer.encode(
            text,
            max_length=max_length,
            padding=padding,
            truncation=truncation,
            return_tensors=return_tensors,
            add_special_tokens=add_special_tokens,
        )
        return result

    def decode(
        self,
        token_ids: list[int] | torch.Tensor,
        skip_special_tokens: bool = True,
        clean_up_tokenization_spaces: bool = True,
    ) -> str:
        if isinstance(token_ids, torch.Tensor):
            token_ids = token_ids.tolist()
        return self._tokenizer.decode(
            token_ids,
            skip_special_tokens=skip_special_tokens,
            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
        )

    def batch_encode(
        self,
        texts: list[str],
        max_length: int | None = None,
        padding: bool | str = True,
        truncation: bool = True,
        return_tensors: str = "pt",
        add_special_tokens: bool = True,
    ) -> BatchEncoding:
        return self._tokenizer(
            texts,
            max_length=max_length,
            padding=padding,
            truncation=truncation,
            return_tensors=return_tensors,
            add_special_tokens=add_special_tokens,
        )

    def batch_decode(
        self,
        token_ids: list[list[int]] | torch.Tensor,
        skip_special_tokens: bool = True,
    ) -> list[str]:
        return self._tokenizer.batch_decode(
            token_ids,
            skip_special_tokens=skip_special_tokens,
        )

    def get_prompt_length(self, prompt: str) -> int:
        return len(self.encode(prompt, add_special_tokens=False))

    def truncate_to_max_length(self, text: str, max_length: int, from_end: bool = False) -> str:
        tokens = self.encode(text, add_special_tokens=False)
        if len(tokens) <= max_length:
            return text

        if from_end:
            tokens = tokens[-max_length:]
        else:
            tokens = tokens[:max_length]

        return self.decode(tokens)

    def __call__(self, text: str | list[str], **kwargs: Any) -> BatchEncoding:
        return self._tokenizer(text, **kwargs)


@dataclass
class PromptTemplate:
    system_prompt: str | None = None
    user_prefix: str = ""
    assistant_prefix: str = ""
    user_suffix: str = ""
    assistant_suffix: str = ""
    separator: str = "\n"

    def format_prompt(self, user_message: str, include_assistant_prefix: bool = True) -> str:
        parts = []

        if self.system_prompt:
            parts.append(self.system_prompt)
            parts.append(self.separator)

        parts.append(self.user_prefix)
        parts.append(user_message)
        parts.append(self.user_suffix)

        if include_assistant_prefix:
            parts.append(self.assistant_prefix)

        return "".join(parts)

    def format_conversation(
        self, turns: list[dict[str, str]], include_assistant_prefix: bool = True
    ) -> str:
        parts = []

        if self.system_prompt:
            parts.append(self.system_prompt)
            parts.append(self.separator)

        for i, turn in enumerate(turns):
            role = turn["role"]
            content = turn["content"]

            if role == "user":
                parts.append(self.user_prefix)
                parts.append(content)
                parts.append(self.user_suffix)
            elif role == "assistant":
                parts.append(self.assistant_prefix)
                parts.append(content)
                parts.append(self.assistant_suffix)

            if i < len(turns) - 1:
                parts.append(self.separator)

        if include_assistant_prefix and turns and turns[-1]["role"] == "user":
            parts.append(self.assistant_prefix)

        return "".join(parts)

    def extract_response(self, full_text: str, prompt: str) -> str:
        if full_text.startswith(prompt):
            response = full_text[len(prompt) :]
        else:
            response = full_text

        response = response.rstrip()
        if response.endswith(self.assistant_suffix):
            response = response[: -len(self.assistant_suffix)]

        return response.strip()

    @classmethod
    def default(cls) -> "PromptTemplate":
        return cls()

    @classmethod
    def llama2_chat(cls) -> "PromptTemplate":
        return cls(
            system_prompt="<<SYS>>\nYou are a helpful assistant.\n<</SYS>>\n\n",
            user_prefix="[INST] ",
            assistant_prefix=" ",
            user_suffix=" [/INST]",
            assistant_suffix="</s>",
            separator="",
        )

    @classmethod
    def chatml(cls) -> "PromptTemplate":
        return cls(
            system_prompt="<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n",
            user_prefix="<|im_start|>user\n",
            assistant_prefix="<|im_start|>assistant\n",
            user_suffix="<|im_end|>\n",
            assistant_suffix="<|im_end|>\n",
            separator="",
        )

    @classmethod
    def alpaca(cls) -> "PromptTemplate":
        return cls(
            system_prompt="Below is an instruction that describes a task. "
            "Write a response that appropriately completes the request.\n\n",
            user_prefix="### Instruction:\n",
            assistant_prefix="### Response:\n",
            user_suffix="\n\n",
            assistant_suffix="\n",
            separator="",
        )

    @classmethod
    def simple(cls, system_prompt: str | None = None) -> "PromptTemplate":
        return cls(
            system_prompt=system_prompt + "\n\n" if system_prompt else None,
            user_prefix="Human: ",
            assistant_prefix="Assistant: ",
            user_suffix="\n",
            assistant_suffix="\n",
            separator="",
        )


class BaseKonicLLMEnvironment(gym.Env, ABC):
    @property
    @abstractmethod
    def tokenizer(self) -> TokenizerWrapper:
        pass

    @property
    @abstractmethod
    def prompt_template(self) -> PromptTemplate:
        pass

    @property
    @abstractmethod
    def generation_config(self) -> "GenerationConfig":
        pass

    @property
    @abstractmethod
    def reward_composer(self) -> "BaseKonicLLMRewardComposer":
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    def compute_reward(self, prompt: str, response: str) -> float:
        pass

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[Any, dict[str, Any]]:
        return super().reset(seed=seed, options=options)

    @abstractmethod
    def step(self, action: int) -> tuple[Any, float, bool, bool, dict]:
        pass


class KonicLLMEnvironment(BaseKonicLLMEnvironment):
    def __init__(
        self,
        model: "PreTrainedModel",
        tokenizer: "PreTrainedTokenizer | TokenizerWrapper",
        reward_composer: "BaseKonicLLMRewardComposer",
        prompt_template: PromptTemplate | None = None,
        generation_config: "GenerationConfig | None" = None,
        max_sequence_length: int = 512,
        max_new_tokens: int = 128,
        device: str | torch.device = "auto",
    ):
        super().__init__()

        from konic.finetuning.config import GenerationConfig as GenConfig

        self._model = model
        self._tokenizer = (
            tokenizer if isinstance(tokenizer, TokenizerWrapper) else TokenizerWrapper(tokenizer)
        )
        self._reward_composer = reward_composer
        self._prompt_template = prompt_template or PromptTemplate.default()
        self._generation_config = generation_config or GenConfig()
        self._max_sequence_length = max_sequence_length
        self._max_new_tokens = max_new_tokens
        self._device = next(model.parameters()).device if device == "auto" else torch.device(device)

        if hasattr(self._reward_composer, "set_env"):
            self._reward_composer.set_env(self)

        self._current_prompt: str = ""
        self._formatted_prompt: str = ""
        self._current_response: str = ""
        self._current_tokens: list[int] = []
        self._prompt_tokens: list[int] = []
        self._response_tokens: list[int] = []
        self._step_count: int = 0
        self._episode_reward: float = 0.0

        self.observation_space: gym.spaces.Space[Any] = gym.spaces.Box(
            low=0,
            high=self._tokenizer.vocab_size - 1,
            shape=(self._max_sequence_length,),
            dtype=np.int64,
        )
        self.action_space: gym.spaces.Space[Any] = gym.spaces.Discrete(self._tokenizer.vocab_size)

    @property
    def tokenizer(self) -> TokenizerWrapper:
        return self._tokenizer

    @property
    def prompt_template(self) -> PromptTemplate:
        return self._prompt_template

    @property
    def generation_config(self) -> "GenerationConfig":
        return self._generation_config

    @property
    def reward_composer(self) -> "BaseKonicLLMRewardComposer":
        return self._reward_composer

    @property
    def model(self) -> "PreTrainedModel":
        return self._model

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[np.ndarray, dict[str, Any]]:
        super().reset(seed=seed, options=options)
        options = options or {}

        if "formatted_prompt" in options:
            self._formatted_prompt = options["formatted_prompt"]
            self._current_prompt = options.get("prompt", self._formatted_prompt)
        elif "prompt" in options:
            self._current_prompt = options["prompt"]
            self._formatted_prompt = self._prompt_template.format_prompt(self._current_prompt)
        else:
            self._current_prompt = ""
            self._formatted_prompt = ""

        if "input_ids" in options:
            self._prompt_tokens = list(options["input_ids"])
        else:
            encoded = self._tokenizer.encode(self._formatted_prompt, add_special_tokens=True)
            self._prompt_tokens = (
                encoded.tolist() if isinstance(encoded, torch.Tensor) else list(encoded)
            )

        self._current_response = ""
        self._response_tokens = []
        self._current_tokens = self._prompt_tokens.copy()
        self._step_count = 0
        self._episode_reward = 0.0

        obs = self._get_observation()
        info = self._get_info()

        return obs, info

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        self._response_tokens.append(action)
        self._current_tokens.append(action)
        self._step_count += 1
        self._current_response = self._tokenizer.decode(
            self._response_tokens, skip_special_tokens=True
        )

        terminated = self._is_terminated(action)
        truncated = self._is_truncated()

        if terminated or truncated:
            reward = self.compute_reward(self._current_prompt, self._current_response)
            self._episode_reward = reward
        else:
            reward = 0.0

        obs = self._get_observation()
        info = self._get_info()
        return obs, reward, terminated, truncated, info

    def generate(self, prompt: str) -> str:
        encoded = self._tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=True)
        input_ids = cast(torch.Tensor, encoded).to(self._device)
        gen_kwargs = self._generation_config.to_dict()
        gen_kwargs["pad_token_id"] = self._tokenizer.pad_token_id
        gen_kwargs["eos_token_id"] = self._tokenizer.eos_token_id

        with torch.no_grad():
            output_ids: torch.Tensor = self._model.generate(input_ids, **gen_kwargs)  # type: ignore[misc]

        response_ids = output_ids[0, input_ids.shape[1] :]
        return self._tokenizer.decode(response_ids, skip_special_tokens=True)

    def compute_reward(self, prompt: str, response: str) -> float:
        return self._reward_composer.compose(prompt, response)

    def _get_observation(self) -> np.ndarray:
        tokens = self._current_tokens.copy()
        if len(tokens) > self._max_sequence_length:
            tokens = tokens[-self._max_sequence_length :]
        padding_length = self._max_sequence_length - len(tokens)
        if padding_length > 0:
            tokens = tokens + [self._tokenizer.pad_token_id] * padding_length
        return np.array(tokens, dtype=np.int64)

    def _is_terminated(self, last_token: int) -> bool:
        return last_token == self._tokenizer.eos_token_id

    def _is_truncated(self) -> bool:
        return self._step_count >= self._max_new_tokens

    def _get_info(self) -> dict:
        return {
            "prompt": self._current_prompt,
            "formatted_prompt": self._formatted_prompt,
            "response": self._current_response,
            "step_count": self._step_count,
            "prompt_length": len(self._prompt_tokens),
            "response_length": len(self._response_tokens),
            "total_length": len(self._current_tokens),
            "episode_reward": self._episode_reward,
        }

    def get_obs(self) -> np.ndarray:
        return self._get_observation()

    def get_info(self) -> dict:
        return self._get_info()

    def render(self) -> None:
        print(f"Prompt: {self._current_prompt}")
        print(f"Response: {self._current_response}")
        print(f"Step: {self._step_count}/{self._max_new_tokens}")

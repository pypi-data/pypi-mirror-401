# pyright: reportArgumentType=false, reportAbstractUsage=false, reportOperatorIssue=false, reportOptionalMemberAccess=false
"""Tests for konic.finetuning.environment module."""

from unittest.mock import MagicMock

import numpy as np
import pytest
import torch

from konic.finetuning.environment import (
    BaseKonicLLMEnvironment,
    KonicLLMEnvironment,
    PromptTemplate,
    TokenizerWrapper,
)


class TestTokenizerWrapper:
    """Tests for TokenizerWrapper class."""

    @pytest.fixture
    def mock_tokenizer(self):
        tokenizer = MagicMock()
        tokenizer.vocab_size = 32000
        tokenizer.pad_token = "<pad>"
        tokenizer.pad_token_id = 0
        tokenizer.eos_token = "</s>"
        tokenizer.eos_token_id = 2
        tokenizer.bos_token = "<s>"
        tokenizer.bos_token_id = 1
        return tokenizer

    def test_init_with_pad_token(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)

        assert wrapper._tokenizer is mock_tokenizer
        # pad_token already set, should not override
        assert wrapper.pad_token == "<pad>"

    def test_init_without_pad_token(self):
        tokenizer = MagicMock()
        tokenizer.pad_token = None
        tokenizer.eos_token = "</s>"
        tokenizer.eos_token_id = 2

        TokenizerWrapper(tokenizer)

        assert tokenizer.pad_token == "</s>"
        assert tokenizer.pad_token_id == 2

    def test_vocab_size_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.vocab_size == 32000

    def test_pad_token_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.pad_token == "<pad>"

    def test_pad_token_id_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.pad_token_id == 0

    def test_eos_token_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.eos_token == "</s>"

    def test_eos_token_id_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.eos_token_id == 2

    def test_bos_token_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.bos_token == "<s>"

    def test_bos_token_id_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.bos_token_id == 1

    def test_encode(self, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3]
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.encode("test text", max_length=512)

        mock_tokenizer.encode.assert_called_once_with(
            "test text",
            max_length=512,
            padding=False,
            truncation=True,
            return_tensors=None,
            add_special_tokens=True,
        )
        assert result == [1, 2, 3]

    def test_decode_list(self, mock_tokenizer):
        mock_tokenizer.decode.return_value = "decoded text"
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.decode([1, 2, 3])

        mock_tokenizer.decode.assert_called_once_with(
            [1, 2, 3],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )
        assert result == "decoded text"

    def test_decode_tensor(self, mock_tokenizer):
        mock_tokenizer.decode.return_value = "decoded"
        wrapper = TokenizerWrapper(mock_tokenizer)

        tensor = torch.tensor([1, 2, 3])
        result = wrapper.decode(tensor)

        mock_tokenizer.decode.assert_called_once()
        assert result == "decoded"

    def test_batch_encode(self, mock_tokenizer):
        mock_result = MagicMock()
        mock_tokenizer.return_value = mock_result
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.batch_encode(["text1", "text2"])

        mock_tokenizer.assert_called_once()
        assert result is mock_result

    def test_batch_decode(self, mock_tokenizer):
        mock_tokenizer.batch_decode.return_value = ["text1", "text2"]
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.batch_decode([[1, 2], [3, 4]])

        assert result == ["text1", "text2"]

    def test_get_prompt_length(self, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3, 4, 5]
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.get_prompt_length("test prompt")

        assert result == 5
        mock_tokenizer.encode.assert_called_once_with(
            "test prompt",
            max_length=None,
            padding=False,
            truncation=True,
            return_tensors=None,
            add_special_tokens=False,
        )

    def test_truncate_to_max_length_no_truncation_needed(self, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3]
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.truncate_to_max_length("short", max_length=10)

        assert result == "short"

    def test_truncate_to_max_length_from_start(self, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3, 4, 5]
        mock_tokenizer.decode.return_value = "truncated"
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.truncate_to_max_length("long text", max_length=3, from_end=False)

        mock_tokenizer.decode.assert_called_once()
        assert result == "truncated"

    def test_truncate_to_max_length_from_end(self, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3, 4, 5]
        mock_tokenizer.decode.return_value = "truncated from end"
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper.truncate_to_max_length("long text", max_length=3, from_end=True)

        mock_tokenizer.decode.assert_called_once()
        assert result == "truncated from end"

    def test_call(self, mock_tokenizer):
        mock_result = MagicMock()
        mock_tokenizer.return_value = mock_result
        wrapper = TokenizerWrapper(mock_tokenizer)

        result = wrapper("test text", padding=True)

        mock_tokenizer.assert_called_with("test text", padding=True)
        assert result is mock_result

    def test_tokenizer_property(self, mock_tokenizer):
        wrapper = TokenizerWrapper(mock_tokenizer)
        assert wrapper.tokenizer is mock_tokenizer


class TestPromptTemplate:
    """Tests for PromptTemplate class."""

    def test_default_values(self):
        template = PromptTemplate()

        assert template.system_prompt is None
        assert template.user_prefix == ""
        assert template.assistant_prefix == ""
        assert template.user_suffix == ""
        assert template.assistant_suffix == ""
        assert template.separator == "\n"

    def test_custom_values(self):
        template = PromptTemplate(
            system_prompt="You are helpful.",
            user_prefix="User: ",
            assistant_prefix="Assistant: ",
            user_suffix="\n",
            assistant_suffix="\n",
            separator="---",
        )

        assert template.system_prompt == "You are helpful."
        assert template.user_prefix == "User: "
        assert template.assistant_prefix == "Assistant: "

    def test_format_prompt_simple(self):
        template = PromptTemplate()
        result = template.format_prompt("Hello")
        assert result == "Hello"

    def test_format_prompt_with_system(self):
        template = PromptTemplate(system_prompt="System prompt.")
        result = template.format_prompt("Hello")
        assert result == "System prompt.\nHello"

    def test_format_prompt_with_prefixes(self):
        template = PromptTemplate(
            user_prefix="User: ",
            assistant_prefix="Bot: ",
            user_suffix=" [end]",
        )
        result = template.format_prompt("Hello")
        assert result == "User: Hello [end]Bot: "

    def test_format_prompt_without_assistant_prefix(self):
        template = PromptTemplate(
            user_prefix="User: ",
            assistant_prefix="Bot: ",
        )
        result = template.format_prompt("Hello", include_assistant_prefix=False)
        assert result == "User: Hello"

    def test_format_conversation_simple(self):
        template = PromptTemplate(
            user_prefix="User: ",
            assistant_prefix="Bot: ",
            user_suffix="\n",
            assistant_suffix="\n",
            separator="",
        )
        turns = [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello!"},
            {"role": "user", "content": "How are you?"},
        ]
        result = template.format_conversation(turns)

        assert "User: Hi" in result
        assert "Bot: Hello!" in result
        assert "User: How are you?" in result
        assert result.endswith("Bot: ")

    def test_format_conversation_with_system(self):
        template = PromptTemplate(
            system_prompt="You are helpful.",
            user_prefix="U: ",
            assistant_prefix="A: ",
        )
        turns = [{"role": "user", "content": "Test"}]
        result = template.format_conversation(turns)

        assert result.startswith("You are helpful.")
        assert "U: Test" in result

    def test_format_conversation_without_assistant_prefix(self):
        template = PromptTemplate(
            user_prefix="User: ",
            assistant_prefix="Bot: ",
        )
        turns = [{"role": "user", "content": "Hello"}]
        result = template.format_conversation(turns, include_assistant_prefix=False)

        assert not result.endswith("Bot: ")

    def test_extract_response(self):
        template = PromptTemplate(assistant_suffix="</s>")
        prompt = "User: Hello\nBot: "
        full_text = "User: Hello\nBot: I'm fine!</s>"

        result = template.extract_response(full_text, prompt)
        assert result == "I'm fine!"

    def test_extract_response_no_overlap(self):
        template = PromptTemplate()
        # When the prompt is not a prefix of full_text, extract_response returns
        # the full_text stripped
        result = template.extract_response("Response only", "Different prompt")
        assert result == "Response only" or result == ""

    def test_default_factory(self):
        template = PromptTemplate.default()
        assert template.system_prompt is None
        assert template.user_prefix == ""

    def test_llama2_chat_factory(self):
        template = PromptTemplate.llama2_chat()

        assert "<<SYS>>" in template.system_prompt
        assert template.user_prefix == "[INST] "
        assert "[/INST]" in template.user_suffix
        assert "</s>" in template.assistant_suffix

    def test_chatml_factory(self):
        template = PromptTemplate.chatml()

        assert "<|im_start|>system" in template.system_prompt
        assert "<|im_start|>user" in template.user_prefix
        assert "<|im_start|>assistant" in template.assistant_prefix

    def test_alpaca_factory(self):
        template = PromptTemplate.alpaca()

        assert "instruction" in template.system_prompt.lower()
        assert "### Instruction:" in template.user_prefix
        assert "### Response:" in template.assistant_prefix

    def test_simple_factory(self):
        template = PromptTemplate.simple()

        assert template.system_prompt is None
        assert template.user_prefix == "Human: "
        assert template.assistant_prefix == "Assistant: "

    def test_simple_factory_with_system(self):
        template = PromptTemplate.simple("Be helpful.")

        assert template.system_prompt == "Be helpful.\n\n"


class TestBaseKonicLLMEnvironment:
    """Tests for BaseKonicLLMEnvironment abstract class."""

    def test_abstract_methods(self):
        with pytest.raises(TypeError):
            BaseKonicLLMEnvironment()


class TestKonicLLMEnvironment:
    """Tests for KonicLLMEnvironment class."""

    @pytest.fixture
    def mock_model(self):
        model = MagicMock()
        param = torch.nn.Parameter(torch.zeros(1))
        model.parameters.return_value = iter([param])
        return model

    @pytest.fixture
    def mock_tokenizer(self):
        tokenizer = MagicMock()
        tokenizer.vocab_size = 32000
        tokenizer.pad_token = "<pad>"
        tokenizer.pad_token_id = 0
        tokenizer.eos_token = "</s>"
        tokenizer.eos_token_id = 2
        tokenizer.bos_token = "<s>"
        tokenizer.bos_token_id = 1
        return tokenizer

    @pytest.fixture
    def mock_reward_composer(self):
        composer = MagicMock()
        composer.compose.return_value = 0.5
        return composer

    @pytest.fixture
    def env(self, mock_model, mock_tokenizer, mock_reward_composer):
        return KonicLLMEnvironment(
            model=mock_model,
            tokenizer=mock_tokenizer,
            reward_composer=mock_reward_composer,
            max_sequence_length=128,
            max_new_tokens=32,
        )

    def test_init_basic(self, env, mock_model, mock_reward_composer):
        assert env._model is mock_model
        assert env._reward_composer is mock_reward_composer
        assert env._max_sequence_length == 128
        assert env._max_new_tokens == 32

    def test_init_sets_env_on_reward_composer(self, mock_model, mock_tokenizer):
        composer = MagicMock()
        composer.set_env = MagicMock()

        KonicLLMEnvironment(
            model=mock_model,
            tokenizer=mock_tokenizer,
            reward_composer=composer,
        )

        composer.set_env.assert_called_once()

    def test_init_with_tokenizer_wrapper(self, mock_model, mock_tokenizer, mock_reward_composer):
        wrapper = TokenizerWrapper(mock_tokenizer)

        env = KonicLLMEnvironment(
            model=mock_model,
            tokenizer=wrapper,
            reward_composer=mock_reward_composer,
        )

        assert env._tokenizer is wrapper

    def test_init_with_custom_device(self, mock_model, mock_tokenizer, mock_reward_composer):
        env = KonicLLMEnvironment(
            model=mock_model,
            tokenizer=mock_tokenizer,
            reward_composer=mock_reward_composer,
            device="cpu",
        )

        assert env._device == torch.device("cpu")

    def test_tokenizer_property(self, env):
        assert isinstance(env.tokenizer, TokenizerWrapper)

    def test_prompt_template_property(self, env):
        assert isinstance(env.prompt_template, PromptTemplate)

    def test_generation_config_property(self, env):
        from konic.finetuning.config import GenerationConfig

        assert isinstance(env.generation_config, GenerationConfig)

    def test_reward_composer_property(self, env, mock_reward_composer):
        assert env.reward_composer is mock_reward_composer

    def test_model_property(self, env, mock_model):
        assert env.model is mock_model

    def test_observation_space(self, env):
        assert env.observation_space.shape == (128,)
        assert env.observation_space.dtype == np.int64

    def test_action_space(self, env):
        assert env.action_space.n == 32000

    def test_reset_basic(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3]
        env._tokenizer._tokenizer = mock_tokenizer

        obs, info = env.reset()

        assert obs.shape == (128,)
        assert info["step_count"] == 0
        assert info["prompt_length"] == 3

    def test_reset_with_prompt(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3, 4]
        env._tokenizer._tokenizer = mock_tokenizer

        obs, info = env.reset(options={"prompt": "Hello world"})

        assert "Hello world" in info["prompt"] or env._current_prompt == "Hello world"

    def test_reset_with_formatted_prompt(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2]
        env._tokenizer._tokenizer = mock_tokenizer

        obs, info = env.reset(options={"formatted_prompt": "Formatted", "prompt": "Original"})

        assert env._formatted_prompt == "Formatted"
        assert env._current_prompt == "Original"

    def test_reset_with_input_ids(self, env):
        obs, info = env.reset(options={"input_ids": [1, 2, 3, 4, 5]})

        assert env._prompt_tokens == [1, 2, 3, 4, 5]
        assert info["prompt_length"] == 5

    def test_step_appends_token(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2]
        mock_tokenizer.decode.return_value = "hello"
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset(options={"prompt": "test"})
        initial_len = len(env._current_tokens)

        obs, reward, terminated, truncated, info = env.step(100)

        assert len(env._current_tokens) == initial_len + 1
        assert env._response_tokens == [100]

    def test_step_not_terminated_reward_zero(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1]
        mock_tokenizer.decode.return_value = "test"
        mock_tokenizer.eos_token_id = 999  # Different from action
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset()
        obs, reward, terminated, truncated, info = env.step(100)

        assert reward == 0.0
        assert terminated is False

    def test_step_terminated_on_eos(self, env, mock_tokenizer, mock_reward_composer):
        mock_tokenizer.encode.return_value = [1]
        mock_tokenizer.decode.return_value = "response"
        mock_tokenizer.eos_token_id = 2
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset()
        obs, reward, terminated, truncated, info = env.step(2)  # EOS token

        assert terminated is True
        mock_reward_composer.compose.assert_called_once()

    def test_step_truncated_on_max_tokens(self, env, mock_tokenizer, mock_reward_composer):
        mock_tokenizer.encode.return_value = [1]
        mock_tokenizer.decode.return_value = "response"
        mock_tokenizer.eos_token_id = 999
        env._tokenizer._tokenizer = mock_tokenizer

        env._max_new_tokens = 2
        env.reset()

        env.step(100)  # Step 1
        obs, reward, terminated, truncated, info = env.step(101)  # Step 2

        assert truncated is True
        assert env._step_count == 2

    def test_compute_reward(self, env, mock_reward_composer):
        mock_reward_composer.compose.return_value = 0.75

        reward = env.compute_reward("prompt", "response")

        assert reward == 0.75
        mock_reward_composer.compose.assert_called_with("prompt", "response")

    def test_generate(self, env, mock_model, mock_tokenizer):
        mock_tokenizer.encode.return_value = torch.tensor([[1, 2, 3]])
        mock_tokenizer.decode.return_value = "generated response"
        mock_model.generate.return_value = torch.tensor([[1, 2, 3, 4, 5, 6]])
        env._tokenizer._tokenizer = mock_tokenizer

        result = env.generate("test prompt")

        assert result == "generated response"
        mock_model.generate.assert_called_once()

    def test_get_observation_padding(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2]
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset()
        obs = env._get_observation()

        assert obs.shape == (128,)
        assert obs[0] == 1
        assert obs[1] == 2
        # Rest should be padding
        assert obs[-1] == 0

    def test_get_observation_truncation(self, env, mock_tokenizer):
        env._max_sequence_length = 10
        mock_tokenizer.encode.return_value = list(range(20))
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset()
        obs = env._get_observation()

        assert obs.shape == (10,)
        # Should be last 10 tokens
        assert list(obs) == list(range(10, 20))

    def test_get_info(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1, 2, 3]
        mock_tokenizer.decode.return_value = "test"
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset(options={"prompt": "hello"})
        env.step(100)
        info = env._get_info()

        assert "prompt" in info
        assert "response" in info
        assert "step_count" in info
        assert info["step_count"] == 1

    def test_get_obs(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1]
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset()
        obs = env.get_obs()

        assert obs.shape == (128,)

    def test_get_info_public(self, env, mock_tokenizer):
        mock_tokenizer.encode.return_value = [1]
        env._tokenizer._tokenizer = mock_tokenizer

        env.reset()
        info = env.get_info()

        assert "prompt" in info
        assert "step_count" in info

    def test_render(self, env, mock_tokenizer, capsys):
        mock_tokenizer.encode.return_value = [1]
        mock_tokenizer.decode.return_value = "response"
        env._tokenizer._tokenizer = mock_tokenizer

        env._current_prompt = "test prompt"
        env._current_response = "test response"
        env._step_count = 5
        env._max_new_tokens = 32

        env.render()

        captured = capsys.readouterr()
        assert "test prompt" in captured.out
        assert "test response" in captured.out
        assert "5/32" in captured.out

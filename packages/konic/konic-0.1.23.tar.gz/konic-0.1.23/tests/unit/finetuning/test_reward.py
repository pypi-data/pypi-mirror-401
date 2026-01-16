# pyright: reportOptionalMemberAccess=false, reportAbstractUsage=false
"""Tests for konic.finetuning.reward module."""

from unittest.mock import MagicMock, patch

import pytest

from konic.common.errors import KonicValidationError
from konic.finetuning.reward import (
    BaseKonicLLMRewardComposer,
    BaseRewardModel,
    BaseRewardReducer,
    KonicLLMRewardComposer,
    LLMRewardKeys,
    MaxReducer,
    MeanReducer,
    WeightedSumReducer,
    get_llm_reward_fns,
    llm_reward,
)


class TestLLMRewardKeys:
    """Tests for LLMRewardKeys enum."""

    def test_custom_reward_fn_attr_key(self):
        assert LLMRewardKeys.CUSTOM_REWARD_FN_ATTR_KEY.value == "_is_llm_reward_fn"


class TestLlmRewardDecorator:
    """Tests for the @llm_reward decorator."""

    def test_decorator_marks_function(self):
        @llm_reward
        def my_reward(prompt: str, response: str) -> float:
            return 1.0

        assert hasattr(my_reward, "_is_llm_reward_fn")
        assert getattr(my_reward, "_is_llm_reward_fn") is True

    def test_decorated_function_executes(self):
        @llm_reward
        def length_reward(prompt: str, response: str) -> float:
            return len(response) / 100.0

        result = length_reward("test", "hello world")
        assert result == len("hello world") / 100.0

    def test_decorator_preserves_function_name(self):
        @llm_reward
        def my_custom_reward(prompt: str, response: str) -> float:
            return 0.5

        assert my_custom_reward.__name__ == "my_custom_reward"


class TestGetLlmRewardFns:
    """Tests for get_llm_reward_fns function."""

    def test_finds_decorated_methods(self):
        class TestComposer:
            @llm_reward
            def reward_a(self, prompt: str, response: str) -> float:
                return 1.0

            @llm_reward
            def reward_b(self, prompt: str, response: str) -> float:
                return 2.0

            def not_a_reward(self, x: int) -> int:
                return x

        composer = TestComposer()
        fns = get_llm_reward_fns(composer)
        fn_names = [fn.__name__ for fn in fns]

        assert len(fns) == 2
        assert "reward_a" in fn_names
        assert "reward_b" in fn_names
        assert "not_a_reward" not in fn_names

    def test_ignores_private_methods(self):
        class TestComposer:
            @llm_reward
            def _private_reward(self, prompt: str, response: str) -> float:
                return 1.0

        composer = TestComposer()
        fns = get_llm_reward_fns(composer)
        assert len(fns) == 0

    def test_empty_object_returns_empty_list(self):
        class EmptyComposer:
            pass

        composer = EmptyComposer()
        fns = get_llm_reward_fns(composer)
        assert fns == []


class TestWeightedSumReducer:
    """Tests for WeightedSumReducer class."""

    def test_reduce_with_default_weights(self):
        reducer = WeightedSumReducer()
        rewards = {"a": 1.0, "b": 2.0, "c": 3.0}
        result = reducer.reduce(rewards)
        assert result == 6.0

    def test_reduce_with_custom_weights(self):
        reducer = WeightedSumReducer(weights={"a": 2.0, "b": 0.5})
        rewards = {"a": 1.0, "b": 2.0, "c": 3.0}
        result = reducer.reduce(rewards)
        # a: 1.0 * 2.0 = 2.0
        # b: 2.0 * 0.5 = 1.0
        # c: 3.0 * 1.0 (default) = 3.0
        assert result == 6.0

    def test_reduce_with_custom_default_weight(self):
        reducer = WeightedSumReducer(default_weight=0.5)
        rewards = {"a": 2.0, "b": 4.0}
        result = reducer.reduce(rewards)
        assert result == 3.0

    def test_reduce_empty_rewards(self):
        reducer = WeightedSumReducer()
        result = reducer.reduce({})
        assert result == 0.0

    def test_reduce_single_reward(self):
        reducer = WeightedSumReducer()
        result = reducer.reduce({"x": 5.0})
        assert result == 5.0


class TestMeanReducer:
    """Tests for MeanReducer class."""

    def test_reduce_multiple_rewards(self):
        reducer = MeanReducer()
        rewards = {"a": 1.0, "b": 2.0, "c": 3.0}
        result = reducer.reduce(rewards)
        assert result == 2.0

    def test_reduce_empty_rewards(self):
        reducer = MeanReducer()
        result = reducer.reduce({})
        assert result == 0.0

    def test_reduce_single_reward(self):
        reducer = MeanReducer()
        result = reducer.reduce({"x": 5.0})
        assert result == 5.0


class TestMaxReducer:
    """Tests for MaxReducer class."""

    def test_reduce_multiple_rewards(self):
        reducer = MaxReducer()
        rewards = {"a": 1.0, "b": 3.0, "c": 2.0}
        result = reducer.reduce(rewards)
        assert result == 3.0

    def test_reduce_empty_rewards(self):
        reducer = MaxReducer()
        result = reducer.reduce({})
        assert result == 0.0

    def test_reduce_single_reward(self):
        reducer = MaxReducer()
        result = reducer.reduce({"x": 5.0})
        assert result == 5.0

    def test_reduce_with_negative_values(self):
        reducer = MaxReducer()
        rewards = {"a": -1.0, "b": -3.0, "c": -2.0}
        result = reducer.reduce(rewards)
        assert result == -1.0


class TestBaseRewardModel:
    """Tests for BaseRewardModel abstract class."""

    def test_repr(self):
        class ConcreteRewardModel(BaseRewardModel):
            @property
            def name(self) -> str:
                return "test_model"

            def compute_reward(self, prompt: str, response: str, **kwargs) -> float:
                return 1.0

        model = ConcreteRewardModel()
        assert repr(model) == "ConcreteRewardModel(name='test_model')"


class TestBaseKonicLLMRewardComposer:
    """Tests for BaseKonicLLMRewardComposer abstract class."""

    def test_set_env(self):
        class ConcreteComposer(BaseKonicLLMRewardComposer):
            def compose(self, prompt: str, response: str) -> float:
                return 0.0

        composer = ConcreteComposer()
        assert composer.env is None

        mock_env = MagicMock()
        composer.set_env(mock_env)
        assert composer.env is mock_env

    def test_compose_batch_default(self):
        class ConcreteComposer(BaseKonicLLMRewardComposer):
            def compose(self, prompt: str, response: str) -> float:
                return len(response) * 0.1

        composer = ConcreteComposer()
        prompts = ["a", "b"]
        responses = ["hello", "world!"]

        rewards, breakdowns = composer.compose_batch(prompts, responses)
        assert len(rewards) == 2
        assert rewards[0] == pytest.approx(0.5)  # len("hello") * 0.1
        assert rewards[1] == pytest.approx(0.6)  # len("world!") * 0.1
        assert breakdowns == {}

    def test_get_reward_breakdown_default(self):
        class ConcreteComposer(BaseKonicLLMRewardComposer):
            def compose(self, prompt: str, response: str) -> float:
                return 0.0

        composer = ConcreteComposer()
        result = composer.get_reward_breakdown("test", "response")
        assert result == {}


class TestKonicLLMRewardComposer:
    """Tests for KonicLLMRewardComposer class."""

    def test_init_defaults(self):
        composer = KonicLLMRewardComposer()
        assert composer._reward_models == []
        assert composer._reward_weights == {}
        assert composer._kl_penalty_weight == 0.0
        assert composer.reducer == WeightedSumReducer

    def test_init_with_kl_penalty(self):
        composer = KonicLLMRewardComposer(kl_penalty_weight=0.1)
        assert composer.kl_penalty_weight == 0.1

    def test_kl_penalty_weight_setter(self):
        composer = KonicLLMRewardComposer()
        composer.kl_penalty_weight = 0.5
        assert composer.kl_penalty_weight == 0.5

    def test_add_reward_model(self):
        composer = KonicLLMRewardComposer()

        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "test_model"

        result = composer.add_reward_model(mock_model, weight=2.0)
        assert result is composer  # Returns self for chaining
        assert mock_model in composer._reward_models
        assert composer._reward_weights["test_model"] == 2.0

    def test_set_reward_weight(self):
        composer = KonicLLMRewardComposer()
        result = composer.set_reward_weight("custom", 1.5)
        assert result is composer
        assert composer._reward_weights["custom"] == 1.5

    def test_compose_with_custom_reward_functions(self):
        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def length_reward(self, prompt: str, response: str) -> float:
                return len(response) / 10.0

            @llm_reward
            def contains_hello(self, prompt: str, response: str) -> float:
                return 1.0 if "hello" in response.lower() else 0.0

        composer = TestComposer()
        reward = composer.compose("test", "hello world")

        # WeightedSumReducer with default weight 1.0
        expected = (len("hello world") / 10.0) + 1.0
        assert reward == expected

    def test_compose_with_custom_function_returning_dict(self):
        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def multi_reward(self, prompt: str, response: str) -> dict:
                return {"length": len(response) / 10.0, "bonus": 0.5}

        composer = TestComposer()
        reward = composer.compose("test", "hello")

        expected = (5 / 10.0) + 0.5
        assert reward == expected

    def test_compose_with_reward_model(self):
        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "mock_reward"
        mock_model.compute_reward.return_value = 0.8

        composer = KonicLLMRewardComposer(reward_models=[mock_model])
        reward = composer.compose("test prompt", "test response")

        mock_model.compute_reward.assert_called_once_with("test prompt", "test response")
        assert reward == 0.8

    def test_compose_handles_reward_model_error(self):
        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "failing_model"
        mock_model.compute_reward.side_effect = RuntimeError("Model error")

        composer = KonicLLMRewardComposer(reward_models=[mock_model])
        reward = composer.compose("test", "response")

        # Should return 0.0 for the failed model
        assert reward == 0.0

    def test_compose_handles_custom_function_error(self):
        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def failing_reward(self, prompt: str, response: str) -> float:
                raise ValueError("Custom error")

        composer = TestComposer()
        reward = composer.compose("test", "response")
        assert reward == 0.0  # Should not raise, just log warning

    def test_compose_with_mean_reducer(self):
        class TestComposer(KonicLLMRewardComposer):
            reducer = MeanReducer

            @llm_reward
            def reward_a(self, prompt: str, response: str) -> float:
                return 1.0

            @llm_reward
            def reward_b(self, prompt: str, response: str) -> float:
                return 3.0

        composer = TestComposer()
        reward = composer.compose("test", "response")
        assert reward == 2.0

    def test_compose_batch_validates_length_mismatch(self):
        composer = KonicLLMRewardComposer()
        with pytest.raises(KonicValidationError) as exc_info:
            composer.compose_batch(["a", "b"], ["x"])
        assert "must have same length" in str(exc_info.value)

    def test_compose_batch_with_custom_rewards(self):
        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def simple_reward(self, prompt: str, response: str) -> float:
                return 1.0

        composer = TestComposer()
        rewards, breakdowns = composer.compose_batch(["a", "b"], ["x", "y"])

        assert len(rewards) == 2
        assert rewards == [1.0, 1.0]
        assert "simple_reward" in breakdowns
        assert breakdowns["simple_reward"] == [1.0, 1.0]

    def test_compose_batch_with_huggingface_model_batch_fallback(self):
        # Test the fallback path when batch computation fails
        mock_model = MagicMock()
        mock_model.name = "hf_model"
        mock_model.compute_reward.return_value = 0.5

        # Make batch_compute_reward fail
        mock_model.batch_compute_reward.side_effect = RuntimeError("Batch failed")

        # Patch isinstance check
        with patch(
            "konic.finetuning.reward.HuggingFaceRewardModel",
            type(mock_model),
        ):
            composer = KonicLLMRewardComposer(reward_models=[mock_model])
            rewards, breakdowns = composer.compose_batch(["a", "b"], ["x", "y"])

        assert len(rewards) == 2

    def test_get_reward_breakdown(self):
        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "model_reward"
        mock_model.compute_reward.return_value = 0.7

        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def custom_reward(self, prompt: str, response: str) -> float:
                return 0.3

        composer = TestComposer(reward_models=[mock_model])
        breakdown = composer.get_reward_breakdown("test", "response")

        assert "model_reward" in breakdown
        assert "custom_reward" in breakdown
        assert breakdown["model_reward"] == 0.7
        assert breakdown["custom_reward"] == 0.3

    def test_compute_kl_penalty(self):
        import torch

        composer = KonicLLMRewardComposer(kl_penalty_weight=0.1)
        log_probs = torch.tensor([1.0, 2.0, 3.0])
        ref_log_probs = torch.tensor([0.5, 1.5, 2.5])

        penalty = composer.compute_kl_penalty(log_probs, ref_log_probs)
        expected = 0.1 * (log_probs - ref_log_probs)

        assert torch.allclose(penalty, expected)


class TestHuggingFaceRewardModel:
    """Tests for HuggingFaceRewardModel class."""

    def test_name_property(self):
        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/reward-model", device="cpu")

            assert model.name == "hf_test_reward_model"

    def test_model_id_property(self):
        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="my/model", device="cpu")

            assert model.model_id == "my/model"

    def test_format_input(self):
        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            result = model._format_input("hello", "world")

            assert result == "hello\nworld"

    def test_compute_reward(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tok.return_value = {"input_ids": torch.tensor([[1, 2, 3]])}
            mock_tok.side_effect = lambda *args, **kwargs: MagicMock(
                to=lambda device: {"input_ids": torch.tensor([[1, 2, 3]])}
            )
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            # Mock the model output
            mock_output = MagicMock()
            mock_output.logits = torch.tensor([[0.5]])  # Single output
            model._model.return_value = mock_output

            reward = model.compute_reward("prompt", "response")

            assert isinstance(reward, float)
            assert reward == 0.5

    def test_cleanup(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            with patch.object(torch.cuda, "is_available", return_value=False):
                model.cleanup()

            assert model._model is None
            assert model._tokenizer is None

    def test_cleanup_with_cuda_available(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            with patch.object(torch.cuda, "is_available", return_value=True):
                with patch.object(torch.cuda, "empty_cache") as mock_empty:
                    model.cleanup()
                    mock_empty.assert_called_once()

    def test_del_method(self):
        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            # __del__ should not raise even if cleanup fails
            model._model = None
            model._tokenizer = None
            del model  # Should not raise

    def test_compute_reward_with_label_index(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tok.side_effect = lambda *args, **kwargs: MagicMock(
                to=lambda device: {"input_ids": torch.tensor([[1, 2, 3]])}
            )
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu", label_index=1)

            # Mock multiple outputs
            mock_output = MagicMock()
            mock_output.logits = torch.tensor([[0.5, 0.8, 0.3]])  # Multiple outputs
            model._model.return_value = mock_output

            reward = model.compute_reward("prompt", "response")

            assert reward == pytest.approx(0.8)

    def test_compute_reward_with_normalization(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tok.side_effect = lambda *args, **kwargs: MagicMock(
                to=lambda device: {"input_ids": torch.tensor([[1, 2, 3]])}
            )
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(
                model_id="test/model",
                device="cpu",
                normalize=True,
                normalize_min=-1.0,
                normalize_max=1.0,
            )

            mock_output = MagicMock()
            mock_output.logits = torch.tensor([[0.5]])
            model._model.return_value = mock_output

            # First call initializes running stats
            reward1 = model.compute_reward("prompt", "response")
            assert isinstance(reward1, float)

    def test_batch_compute_reward(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tok.side_effect = lambda *args, **kwargs: MagicMock(
                to=lambda device: {"input_ids": torch.tensor([[1, 2, 3], [4, 5, 6]])}
            )
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            mock_output = MagicMock()
            mock_output.logits = torch.tensor([[0.5], [0.7]])
            model._model.return_value = mock_output

            rewards = model.batch_compute_reward(["p1", "p2"], ["r1", "r2"])

            assert len(rewards) == 2
            assert rewards[0] == pytest.approx(0.5)
            assert rewards[1] == pytest.approx(0.7)

    def test_batch_compute_reward_length_mismatch(self):
        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu")

            with pytest.raises(KonicValidationError) as exc_info:
                model.batch_compute_reward(["p1", "p2"], ["r1"])
            assert "same length" in str(exc_info.value)

    def test_batch_compute_reward_with_label_index(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tok.side_effect = lambda *args, **kwargs: MagicMock(
                to=lambda device: {"input_ids": torch.tensor([[1, 2], [3, 4]])}
            )
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu", label_index=1)

            mock_output = MagicMock()
            mock_output.logits = torch.tensor([[0.1, 0.5], [0.2, 0.7]])
            model._model.return_value = mock_output

            rewards = model.batch_compute_reward(["p1", "p2"], ["r1", "r2"])

            assert rewards[0] == pytest.approx(0.5)
            assert rewards[1] == pytest.approx(0.7)

    def test_batch_compute_reward_with_normalization(self):
        import torch

        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = "</s>"
            mock_tok.side_effect = lambda *args, **kwargs: MagicMock(
                to=lambda device: {"input_ids": torch.tensor([[1], [2]])}
            )
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            model = HuggingFaceRewardModel(model_id="test/model", device="cpu", normalize=True)

            mock_output = MagicMock()
            mock_output.logits = torch.tensor([[0.5], [0.7]])
            model._model.return_value = mock_output

            rewards = model.batch_compute_reward(["p1", "p2"], ["r1", "r2"])

            assert len(rewards) == 2

    def test_pad_token_set_to_eos_when_none(self):
        with (
            patch("transformers.AutoModelForSequenceClassification") as mock_auto_model,
            patch("transformers.AutoTokenizer") as mock_tokenizer,
        ):
            mock_model = MagicMock()
            mock_model.parameters.return_value = iter([MagicMock()])
            mock_auto_model.from_pretrained.return_value = mock_model

            mock_tok = MagicMock()
            mock_tok.pad_token = None
            mock_tok.eos_token = "</s>"
            mock_tokenizer.from_pretrained.return_value = mock_tok

            from konic.finetuning.reward import HuggingFaceRewardModel

            HuggingFaceRewardModel(model_id="test/model", device="cpu")

            assert mock_tok.pad_token == "</s>"


class TestGetLlmRewardFnsEdgeCases:
    """Additional tests for get_llm_reward_fns edge cases."""

    def test_handles_attribute_error(self):
        class ProblematicObj:
            @property
            def problematic_attr(self):
                raise AttributeError("Cannot access")

        obj = ProblematicObj()
        fns = get_llm_reward_fns(obj)
        assert fns == []


class TestKonicLLMRewardComposerEdgeCases:
    """Additional edge case tests for KonicLLMRewardComposer."""

    def test_compose_batch_with_sequential_model(self):
        """Test compose_batch falls back to sequential for non-HF models."""
        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "custom_model"
        mock_model.compute_reward.return_value = 0.5

        composer = KonicLLMRewardComposer(reward_models=[mock_model])
        rewards, breakdowns = composer.compose_batch(["p1", "p2"], ["r1", "r2"])

        assert len(rewards) == 2
        assert mock_model.compute_reward.call_count == 2

    def test_compose_batch_with_huggingface_model_success(self):
        """Test compose_batch uses batch computation for HF models."""
        with patch("konic.finetuning.reward.HuggingFaceRewardModel") as mock_hf:
            mock_model = MagicMock()
            mock_model.name = "hf_model"
            mock_model.batch_compute_reward.return_value = [0.5, 0.6]

            # Make isinstance check return True
            mock_hf.__class__ = type(mock_model)

            composer = KonicLLMRewardComposer(reward_models=[mock_model])

            # Patch isinstance to return True for our mock
            with patch(
                "konic.finetuning.reward.isinstance", side_effect=lambda obj, cls: obj is mock_model
            ):
                rewards, breakdowns = composer.compose_batch(["p1", "p2"], ["r1", "r2"])

            assert len(rewards) == 2

    def test_compute_model_rewards_sequential_handles_error(self):
        """Test _compute_model_rewards_sequential handles errors gracefully."""
        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "failing_model"
        mock_model.compute_reward.side_effect = RuntimeError("Failed")

        composer = KonicLLMRewardComposer(reward_models=[mock_model])
        rewards_per_sample = [{}, {}]

        composer._compute_model_rewards_sequential(
            mock_model, ["p1", "p2"], ["r1", "r2"], rewards_per_sample
        )

        assert rewards_per_sample[0]["failing_model"] == 0.0
        assert rewards_per_sample[1]["failing_model"] == 0.0

    def test_get_reward_breakdown_handles_model_error(self):
        """Test get_reward_breakdown handles model errors."""
        mock_model = MagicMock(spec=BaseRewardModel)
        mock_model.name = "error_model"
        mock_model.compute_reward.side_effect = RuntimeError("Error")

        composer = KonicLLMRewardComposer(reward_models=[mock_model])
        breakdown = composer.get_reward_breakdown("test", "response")

        assert breakdown["error_model"] == 0.0

    def test_get_reward_breakdown_with_dict_return(self):
        """Test get_reward_breakdown with custom fn returning dict."""

        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def multi_reward(self, prompt: str, response: str) -> dict:
                return {"sub_a": 0.3, "sub_b": 0.7}

        composer = TestComposer()
        breakdown = composer.get_reward_breakdown("test", "response")

        assert "sub_a" in breakdown
        assert "sub_b" in breakdown

    def test_get_reward_breakdown_handles_custom_fn_error(self):
        """Test get_reward_breakdown handles custom function errors."""

        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def failing_fn(self, prompt: str, response: str) -> float:
                raise ValueError("Custom error")

        composer = TestComposer()
        breakdown = composer.get_reward_breakdown("test", "response")

        # Should not contain the failing function key or should be empty
        assert "failing_fn" not in breakdown

    def test_compose_batch_builds_breakdown_dict(self):
        """Test that compose_batch correctly builds breakdown dictionary."""

        class TestComposer(KonicLLMRewardComposer):
            @llm_reward
            def reward_a(self, prompt: str, response: str) -> float:
                return 0.5

            @llm_reward
            def reward_b(self, prompt: str, response: str) -> float:
                return 0.3

        composer = TestComposer()
        rewards, breakdowns = composer.compose_batch(
            ["p1", "p2", "p3"],
            ["r1", "r2", "r3"],
        )

        assert len(rewards) == 3
        assert "reward_a" in breakdowns
        assert "reward_b" in breakdowns
        assert len(breakdowns["reward_a"]) == 3
        assert len(breakdowns["reward_b"]) == 3

    def test_init_with_custom_reducer(self):
        """Test initializing with a custom reducer."""
        composer = KonicLLMRewardComposer(reducer=MeanReducer)
        assert composer.reducer == MeanReducer


class TestBaseRewardReducerAbstract:
    """Tests for BaseRewardReducer abstract class."""

    def test_is_abstract(self):
        from abc import ABC

        assert issubclass(BaseRewardReducer, ABC)

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            BaseRewardReducer()

# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
"""Tests for konic.finetuning.dataset module."""

from unittest.mock import MagicMock, patch

import pytest

from konic.common.errors import (
    KonicConfigurationError,
    KonicEnvironmentError,
    KonicValidationError,
)
from konic.finetuning.dataset import (
    DatasetConfig,
    DatasetLoader,
    DatasetSource,
    PreferenceDatasetConfig,
    PromptDatasetConfig,
)


class TestDatasetSource:
    """Tests for DatasetSource enum."""

    def test_huggingface_value(self):
        assert DatasetSource.HUGGINGFACE.value == "huggingface"

    def test_konic_cloud_value(self):
        assert DatasetSource.KONIC_CLOUD.value == "konic_cloud"


class TestDatasetConfig:
    """Tests for DatasetConfig dataclass."""

    def test_default_values(self):
        config = DatasetConfig(name="test_dataset")
        assert config.source == DatasetSource.HUGGINGFACE
        assert config.name == "test_dataset"
        assert config.prompt_column == "prompt"
        assert config.response_column is None
        assert config.chosen_column is None
        assert config.rejected_column is None
        assert config.split == "train"
        assert config.subset is None
        assert config.streaming is False
        assert config.max_samples is None
        assert config.shuffle is True
        assert config.shuffle_seed == 42
        assert config.preprocessing_fn is None

    def test_validation_empty_name_raises(self):
        with pytest.raises(KonicValidationError) as exc_info:
            DatasetConfig(name="")
        assert "Dataset name must be provided" in str(exc_info.value)

    def test_validation_streaming_with_konic_cloud_raises(self):
        with pytest.raises(KonicConfigurationError) as exc_info:
            DatasetConfig(
                name="test",
                source=DatasetSource.KONIC_CLOUD,
                streaming=True,
            )
        assert "Streaming is not supported" in str(exc_info.value)

    def test_to_dict(self):
        config = DatasetConfig(
            name="test_dataset",
            split="validation",
            max_samples=100,
        )
        result = config.to_dict()

        assert result["source"] == "huggingface"
        assert result["name"] == "test_dataset"
        assert result["split"] == "validation"
        assert result["max_samples"] == 100
        assert result["prompt_column"] == "prompt"

    def test_from_dict(self):
        data = {
            "name": "test_dataset",
            "source": "huggingface",
            "split": "test",
            "max_samples": 50,
        }
        config = DatasetConfig.from_dict(data)

        assert config.name == "test_dataset"
        assert config.source == DatasetSource.HUGGINGFACE
        assert config.split == "test"
        assert config.max_samples == 50

    def test_from_dict_with_enum_source(self):
        data = {
            "name": "test",
            "source": DatasetSource.KONIC_CLOUD,
        }
        config = DatasetConfig.from_dict(data)
        assert config.source == DatasetSource.KONIC_CLOUD


class TestPromptDatasetConfig:
    """Tests for PromptDatasetConfig dataclass."""

    def test_default_values(self):
        config = PromptDatasetConfig(name="test")
        assert config.context_column is None
        assert config.system_prompt is None

    def test_get_prompt_basic(self):
        config = PromptDatasetConfig(name="test", prompt_column="question")
        example = {"question": "What is Python?"}

        result = config.get_prompt(example)
        assert result == "What is Python?"

    def test_get_prompt_with_context(self):
        config = PromptDatasetConfig(
            name="test",
            prompt_column="question",
            context_column="context",
        )
        example = {
            "question": "What is it?",
            "context": "Python is a programming language.",
        }

        result = config.get_prompt(example)
        assert result == "Python is a programming language.\n\nWhat is it?"

    def test_get_prompt_with_system_prompt(self):
        config = PromptDatasetConfig(
            name="test",
            prompt_column="question",
            system_prompt="You are a helpful assistant.",
        )
        example = {"question": "Hello"}

        result = config.get_prompt(example)
        assert result == "You are a helpful assistant.\n\nHello"

    def test_get_prompt_with_context_and_system(self):
        config = PromptDatasetConfig(
            name="test",
            prompt_column="q",
            context_column="ctx",
            system_prompt="Be helpful.",
        )
        example = {"q": "Question", "ctx": "Context"}

        result = config.get_prompt(example)
        assert result == "Be helpful.\n\nContext\n\nQuestion"

    def test_get_prompt_empty_context(self):
        config = PromptDatasetConfig(
            name="test",
            prompt_column="q",
            context_column="ctx",
        )
        example = {"q": "Question", "ctx": ""}

        result = config.get_prompt(example)
        assert result == "Question"

    def test_get_prompt_missing_context_column(self):
        config = PromptDatasetConfig(
            name="test",
            prompt_column="q",
            context_column="ctx",
        )
        example = {"q": "Question"}

        result = config.get_prompt(example)
        assert result == "Question"


class TestPreferenceDatasetConfig:
    """Tests for PreferenceDatasetConfig dataclass."""

    def test_default_values(self):
        config = PreferenceDatasetConfig(name="test")
        assert config.chosen_column == "chosen"
        assert config.rejected_column == "rejected"

    def test_custom_columns(self):
        config = PreferenceDatasetConfig(
            name="test",
            chosen_column="preferred",
            rejected_column="rejected_response",
        )
        assert config.chosen_column == "preferred"
        assert config.rejected_column == "rejected_response"


class TestDatasetLoader:
    """Tests for DatasetLoader class."""

    def test_init(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        assert loader.config is config
        assert loader._dataset is None

    def test_init_with_konic_credentials(self):
        config = DatasetConfig(name="test", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
            konic_api_key="test_key",
        )

        assert loader._konic_api_url == "http://test.api"
        assert loader._konic_api_key == "test_key"

    def test_load_from_huggingface(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.__len__ = MagicMock(return_value=100)
            mock_dataset.select.return_value = mock_dataset
            mock_dataset.shuffle.return_value = mock_dataset
            mock_load_dataset.return_value = mock_dataset

            config = DatasetConfig(name="test/dataset", shuffle=False)
            loader = DatasetLoader(config)
            result = loader.load()

            mock_load_dataset.assert_called_once_with(
                path="test/dataset",
                split="train",
                streaming=False,
            )
            assert result is mock_dataset

    def test_load_with_subset(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.__len__ = MagicMock(return_value=100)
            mock_dataset.select.return_value = mock_dataset
            mock_dataset.shuffle.return_value = mock_dataset
            mock_load_dataset.return_value = mock_dataset

            config = DatasetConfig(name="test", subset="en", shuffle=False)
            loader = DatasetLoader(config)
            loader.load()

            mock_load_dataset.assert_called_once_with(
                path="test",
                split="train",
                streaming=False,
                name="en",
            )

    def test_load_with_max_samples(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.__len__ = MagicMock(return_value=1000)
            mock_dataset.select.return_value = mock_dataset
            mock_dataset.shuffle.return_value = mock_dataset
            mock_load_dataset.return_value = mock_dataset

            config = DatasetConfig(name="test", max_samples=100, shuffle=False)
            loader = DatasetLoader(config)
            loader.load()

            # Should call select with range(100)
            mock_dataset.select.assert_called_once()

    def test_load_with_shuffle(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.__len__ = MagicMock(return_value=100)
            mock_dataset.shuffle.return_value = mock_dataset
            mock_load_dataset.return_value = mock_dataset

            config = DatasetConfig(name="test", shuffle=True, shuffle_seed=123)
            loader = DatasetLoader(config)
            loader.load()

            mock_dataset.shuffle.assert_called_once_with(seed=123)

    def test_load_fails_raises_runtime_error(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_load_dataset.side_effect = Exception("Network error")

            config = DatasetConfig(name="nonexistent")
            loader = DatasetLoader(config)

            with pytest.raises(RuntimeError) as exc_info:
                loader.load()
            assert "Failed to load HuggingFace dataset" in str(exc_info.value)

    def test_load_unsupported_source_raises(self):
        config = DatasetConfig(name="test")
        config.source = MagicMock()  # Invalid source
        loader = DatasetLoader(config)

        with pytest.raises(KonicValidationError) as exc_info:
            loader.load()
        assert "Unsupported dataset source" in str(exc_info.value)

    def test_load_konic_cloud_missing_host_raises(self, monkeypatch):
        monkeypatch.delenv("KONIC_HOST", raising=False)

        config = DatasetConfig(name="test", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(config)

        with pytest.raises(KonicEnvironmentError) as exc_info:
            loader.load()
        assert "KONIC_HOST" in str(exc_info.value)

    def test_iter_batches_loads_dataset_if_needed(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.__len__ = MagicMock(return_value=16)
            mock_dataset.select.return_value = mock_dataset
            mock_dataset.shuffle.return_value = mock_dataset
            mock_dataset.column_names = ["prompt", "response"]
            mock_dataset.__getitem__ = lambda self, key: ["text"] * 8
            mock_load_dataset.return_value = mock_dataset

            config = DatasetConfig(name="test", shuffle=False)
            loader = DatasetLoader(config)

            # Consume one batch
            next(loader.iter_batches(batch_size=8))

            mock_load_dataset.assert_called_once()

    def test_get_prompts(self):
        config = DatasetConfig(name="test", prompt_column="prompt")
        loader = DatasetLoader(config)
        mock_dataset = MagicMock()
        loader._dataset = mock_dataset

        batch = {"prompt": ["hello", "world"], "response": ["hi", "there"]}
        prompts = loader.get_prompts(batch)

        assert prompts == ["hello", "world"]

    def test_get_prompts_missing_column_raises(self):
        config = DatasetConfig(name="test", prompt_column="nonexistent")
        loader = DatasetLoader(config)

        batch = {"prompt": ["test"]}

        with pytest.raises(KeyError) as exc_info:
            loader.get_prompts(batch)
        assert "nonexistent" in str(exc_info.value)

    def test_dataset_property_before_load_raises(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        with pytest.raises(RuntimeError) as exc_info:
            _ = loader.dataset
        assert "Dataset not loaded" in str(exc_info.value)

    def test_len_before_load_raises(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        with pytest.raises(RuntimeError) as exc_info:
            len(loader)
        assert "Dataset not loaded" in str(exc_info.value)

    def test_len_streaming_raises(self):
        config = DatasetConfig(name="test", streaming=True)
        loader = DatasetLoader(config)
        mock_dataset = MagicMock()
        loader._dataset = mock_dataset
        loader.config = config

        with pytest.raises(RuntimeError) as exc_info:
            len(loader)
        assert "Cannot get length of streaming dataset" in str(exc_info.value)

    def test_iter(self):
        mock_dataset = [{"prompt": "a"}, {"prompt": "b"}]

        config = DatasetConfig(name="test", shuffle=False)
        loader = DatasetLoader(config)
        loader._dataset = mock_dataset

        items = list(loader)
        assert len(items) == 2

    def test_register_preprocessing(self):
        @DatasetLoader.register_preprocessing("my_preprocessor")
        def my_fn(example):
            return example

        assert "my_preprocessor" in DatasetLoader._preprocessing_registry

        # Clean up
        del DatasetLoader._preprocessing_registry["my_preprocessor"]

    def test_apply_preprocessing_not_found_raises(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.shuffle.return_value = mock_dataset
            mock_load_dataset.return_value = mock_dataset

            config = DatasetConfig(name="test", preprocessing_fn="nonexistent")
            loader = DatasetLoader(config)

            with pytest.raises(KonicValidationError) as exc_info:
                loader.load()
            assert "Preprocessing function 'nonexistent' not found" in str(exc_info.value)

    def test_apply_preprocessing_success(self):
        with patch("datasets.load_dataset") as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_dataset.map.return_value = mock_dataset
            mock_dataset.shuffle.return_value = mock_dataset
            mock_load_dataset.return_value = mock_dataset

            @DatasetLoader.register_preprocessing("test_preprocess")
            def test_fn(example):
                return example

            config = DatasetConfig(name="test", preprocessing_fn="test_preprocess")
            loader = DatasetLoader(config)
            loader.load()

            mock_dataset.map.assert_called_once_with(test_fn)

            # Clean up
            del DatasetLoader._preprocessing_registry["test_preprocess"]


class TestDatasetLoaderBatching:
    """Tests for DatasetLoader batch iteration."""

    def test_iter_regular_batches(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        # Create mock dataset
        mock_dataset = MagicMock()
        mock_dataset.__len__ = MagicMock(return_value=10)
        mock_dataset.column_names = ["prompt"]

        def mock_select(indices):
            result = MagicMock()
            result.__getitem__ = lambda self, key: [f"item_{i}" for i in indices]
            result.column_names = ["prompt"]
            return result

        mock_dataset.select = mock_select
        loader._dataset = mock_dataset
        loader.config = DatasetConfig(name="test", streaming=False)

        batches = list(loader._iter_regular_batches(batch_size=3, drop_last=False))
        # 10 items with batch_size=3: 3, 3, 3, 1 = 4 batches
        assert len(batches) == 4

    def test_iter_regular_batches_drop_last(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        mock_dataset = MagicMock()
        mock_dataset.__len__ = MagicMock(return_value=10)
        mock_dataset.column_names = ["prompt"]

        def mock_select(indices):
            result = MagicMock()
            result.__getitem__ = lambda self, key: [f"item_{i}" for i in indices]
            result.column_names = ["prompt"]
            return result

        mock_dataset.select = mock_select
        loader._dataset = mock_dataset
        loader.config = DatasetConfig(name="test", streaming=False)

        batches = list(loader._iter_regular_batches(batch_size=3, drop_last=True))
        # 10 items with batch_size=3, drop_last=True: 3 batches
        assert len(batches) == 3

    def test_iter_streaming_batches(self):
        config = DatasetConfig(name="test", streaming=True)
        loader = DatasetLoader(config)

        # Mock streaming dataset
        mock_data = [
            {"prompt": "a"},
            {"prompt": "b"},
            {"prompt": "c"},
            {"prompt": "d"},
            {"prompt": "e"},
        ]
        loader._dataset = iter(mock_data)

        batches = list(loader._iter_streaming_batches(batch_size=2))
        assert len(batches) == 3  # 2, 2, 1
        assert batches[0]["prompt"] == ["a", "b"]
        assert batches[1]["prompt"] == ["c", "d"]
        assert batches[2]["prompt"] == ["e"]

    def test_batch_to_dict(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        batch = [
            {"prompt": "a", "response": "x"},
            {"prompt": "b", "response": "y"},
        ]
        result = loader._batch_to_dict(batch, ["prompt", "response"])

        assert result == {"prompt": ["a", "b"], "response": ["x", "y"]}


class TestRetryWithBackoff:
    """Tests for _retry_with_backoff decorator."""

    def test_retry_succeeds_first_attempt(self):
        from konic.finetuning.dataset import _retry_with_backoff

        call_count = 0

        @_retry_with_backoff(max_retries=3, initial_delay=0.01, retryable_exceptions=(ValueError,))
        def success_fn():
            nonlocal call_count
            call_count += 1
            return "success"

        result = success_fn()
        assert result == "success"
        assert call_count == 1

    def test_retry_succeeds_after_failures(self):
        from konic.finetuning.dataset import _retry_with_backoff

        call_count = 0

        @_retry_with_backoff(max_retries=3, initial_delay=0.01, retryable_exceptions=(ValueError,))
        def eventually_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = eventually_succeeds()
        assert result == "success"
        assert call_count == 3

    def test_retry_exhausts_and_raises(self):
        from konic.finetuning.dataset import _retry_with_backoff

        call_count = 0

        @_retry_with_backoff(max_retries=3, initial_delay=0.01, retryable_exceptions=(ValueError,))
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        with pytest.raises(ValueError) as exc_info:
            always_fails()
        assert "Always fails" in str(exc_info.value)
        assert call_count == 3

    def test_retry_non_retryable_exception_raises_immediately(self):
        from konic.finetuning.dataset import _retry_with_backoff

        call_count = 0

        @_retry_with_backoff(max_retries=3, initial_delay=0.01, retryable_exceptions=(ValueError,))
        def raises_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("Not retryable")

        with pytest.raises(TypeError):
            raises_type_error()
        assert call_count == 1  # Should fail immediately without retry


class TestDatasetLoaderKonicCloud:
    """Tests for Konic Cloud dataset loading."""

    def test_load_from_konic_cloud_success_json(self, monkeypatch):
        config = DatasetConfig(name="test-dataset", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
            konic_api_key="test-key",
        )

        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {
            "download_url": "http://test.api/data/test.json",
            "format": "json",
        }

        mock_data_response = MagicMock()
        mock_data_response.status_code = 200
        mock_data_response.json.return_value = [
            {"prompt": "hello"},
            {"prompt": "world"},
        ]

        with patch("requests.get") as mock_get:
            mock_get.side_effect = [mock_info_response, mock_data_response]

            with patch("datasets.Dataset.from_list") as mock_from_list:
                mock_dataset = MagicMock()
                mock_dataset.shuffle.return_value = mock_dataset
                mock_from_list.return_value = mock_dataset

                result = loader.load()
                assert result is mock_dataset

    def test_load_from_konic_cloud_no_download_url(self, monkeypatch):
        config = DatasetConfig(name="test-dataset", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
        )

        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {}  # No download_url

        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_info_response

            with pytest.raises(KonicValidationError) as exc_info:
                loader.load()
            assert "No download URL" in str(exc_info.value)

    def test_load_from_konic_cloud_parquet_format(self, monkeypatch):
        config = DatasetConfig(name="test-dataset", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
        )

        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {
            "download_url": "http://test.api/data/test.parquet",
            "format": "parquet",
        }

        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_info_response

            with patch("datasets.Dataset.from_parquet") as mock_from_parquet:
                mock_dataset = MagicMock()
                mock_dataset.shuffle.return_value = mock_dataset
                mock_from_parquet.return_value = mock_dataset

                loader.load()
                mock_from_parquet.assert_called_once()

    def test_load_from_konic_cloud_csv_format(self, monkeypatch):
        config = DatasetConfig(name="test-dataset", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
        )

        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {
            "download_url": "http://test.api/data/test.csv",
            "format": "csv",
        }

        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_info_response

            with patch("datasets.Dataset.from_csv") as mock_from_csv:
                mock_dataset = MagicMock()
                mock_dataset.shuffle.return_value = mock_dataset
                mock_from_csv.return_value = mock_dataset

                loader.load()
                mock_from_csv.assert_called_once()

    def test_load_from_konic_cloud_unsupported_format(self, monkeypatch):
        config = DatasetConfig(name="test-dataset", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
        )

        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {
            "download_url": "http://test.api/data/test.txt",
            "format": "txt",
        }

        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_info_response

            with pytest.raises(KonicValidationError) as exc_info:
                loader.load()
            assert "Unsupported data format" in str(exc_info.value)

    def test_load_from_konic_cloud_request_exception(self, monkeypatch):
        import requests

        config = DatasetConfig(name="test-dataset", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(
            config,
            konic_api_url="http://test.api",
        )

        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.RequestException("Network error")

            with pytest.raises(RuntimeError) as exc_info:
                loader.load()
            assert "Failed to load Konic Cloud dataset" in str(exc_info.value)

    def test_load_from_konic_cloud_uses_env_vars(self, monkeypatch):
        monkeypatch.setenv("KONIC_HOST", "http://env.api")
        monkeypatch.setenv("KONIC_API_KEY", "env-key")

        config = DatasetConfig(name="test", source=DatasetSource.KONIC_CLOUD)
        loader = DatasetLoader(config)  # No explicit credentials

        mock_info_response = MagicMock()
        mock_info_response.status_code = 200
        mock_info_response.json.return_value = {
            "download_url": "http://env.api/data/test.json",
            "format": "json",
        }

        mock_data_response = MagicMock()
        mock_data_response.status_code = 200
        mock_data_response.json.return_value = [{"prompt": "test"}]

        with patch("requests.get") as mock_get:
            mock_get.side_effect = [mock_info_response, mock_data_response]

            with patch("datasets.Dataset.from_list") as mock_from_list:
                mock_dataset = MagicMock()
                mock_dataset.shuffle.return_value = mock_dataset
                mock_from_list.return_value = mock_dataset

                loader.load()

                # Check headers were set correctly
                calls = mock_get.call_args_list
                assert "Authorization" in calls[0][1].get("headers", {})


class TestDatasetLoaderAdditional:
    """Additional edge case tests for DatasetLoader."""

    def test_iter_batches_streaming_path(self):
        config = DatasetConfig(name="test", streaming=True)
        loader = DatasetLoader(config)

        mock_data = [{"prompt": "a"}, {"prompt": "b"}]
        loader._dataset = iter(mock_data)
        loader.config = config

        batches = list(loader.iter_batches(batch_size=1))
        assert len(batches) == 2

    def test_get_prompts_none_batch_loads_from_dataset(self):
        config = DatasetConfig(name="test", prompt_column="prompt", shuffle=False)
        loader = DatasetLoader(config)

        mock_dataset = MagicMock()
        mock_dataset.__len__ = MagicMock(return_value=8)
        mock_dataset.column_names = ["prompt"]

        def mock_select(indices):
            result = MagicMock()
            result.__getitem__ = lambda self, key: ["item"] * len(list(indices))
            result.column_names = ["prompt"]
            return result

        mock_dataset.select = mock_select
        loader._dataset = mock_dataset

        # Call get_prompts with None batch
        prompts = loader.get_prompts(None)
        assert isinstance(prompts, list)

    def test_get_prompts_non_list_conversion(self):
        config = DatasetConfig(name="test", prompt_column="prompt")
        loader = DatasetLoader(config)

        # Mock object that's not a list but iterable
        class NotAList:
            def __iter__(self):
                return iter(["a", "b", "c"])

        batch = {"prompt": NotAList()}
        prompts = loader.get_prompts(batch)

        assert isinstance(prompts, list)
        assert prompts == ["a", "b", "c"]

    def test_len_returns_dataset_length(self):
        config = DatasetConfig(name="test")
        loader = DatasetLoader(config)

        mock_dataset = MagicMock()
        mock_dataset.__len__ = MagicMock(return_value=42)
        loader._dataset = mock_dataset
        loader.config = DatasetConfig(name="test", streaming=False)

        assert len(loader) == 42

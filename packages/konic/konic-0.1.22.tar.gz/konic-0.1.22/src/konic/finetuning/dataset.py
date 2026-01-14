"""Dataset loading and configuration for LLM finetuning."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import TYPE_CHECKING, Any

from konic.common.errors import (
    KonicConfigurationError,
    KonicEnvironmentError,
    KonicValidationError,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from datasets import Dataset, IterableDataset


def _retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = (),
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception: Exception | None = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor

            # All retries exhausted
            if last_exception is not None:
                raise last_exception

        return wrapper

    return decorator


class DatasetSource(Enum):
    HUGGINGFACE = "huggingface"
    KONIC_CLOUD = "konic_cloud"


@dataclass
class DatasetConfig:
    source: DatasetSource = DatasetSource.HUGGINGFACE
    name: str = ""
    prompt_column: str = "prompt"
    response_column: str | None = None
    chosen_column: str | None = None
    rejected_column: str | None = None
    split: str = "train"
    subset: str | None = None
    streaming: bool = False
    max_samples: int | None = None

    # Additional processing options
    shuffle: bool = True
    shuffle_seed: int = 42
    preprocessing_fn: str | None = None  # Name of custom preprocessing function

    def __post_init__(self):
        if not self.name:
            raise KonicValidationError(
                "Dataset name must be provided",
                field="name",
            )

        if self.source == DatasetSource.KONIC_CLOUD and self.streaming:
            raise KonicConfigurationError(
                "Streaming is not supported for Konic Cloud datasets",
                config_key="streaming",
            )

    def to_dict(self) -> dict:
        return {
            "source": self.source.value,
            "name": self.name,
            "prompt_column": self.prompt_column,
            "response_column": self.response_column,
            "chosen_column": self.chosen_column,
            "rejected_column": self.rejected_column,
            "split": self.split,
            "subset": self.subset,
            "streaming": self.streaming,
            "max_samples": self.max_samples,
            "shuffle": self.shuffle,
            "shuffle_seed": self.shuffle_seed,
            "preprocessing_fn": self.preprocessing_fn,
        }

    @classmethod
    def from_dict(cls, data: dict) -> DatasetConfig:
        # Handle source enum conversion
        if "source" in data:
            if isinstance(data["source"], str):
                data["source"] = DatasetSource(data["source"])

        return cls(**data)


@dataclass
class PromptDatasetConfig(DatasetConfig):
    context_column: str | None = None
    system_prompt: str | None = None

    def get_prompt(self, example: dict) -> str:
        prompt = example.get(self.prompt_column, "")

        # Add context if available
        if self.context_column and self.context_column in example:
            context = example[self.context_column]
            if context:
                prompt = f"{context}\n\n{prompt}"

        # Add system prompt if specified
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"

        return prompt


@dataclass
class PreferenceDatasetConfig(DatasetConfig):
    chosen_column: str | None = "chosen"  # type: ignore[assignment]
    rejected_column: str | None = "rejected"  # type: ignore[assignment]


class DatasetLoader:
    _preprocessing_registry: dict[str, Callable] = {}

    def __init__(
        self,
        config: DatasetConfig,
        konic_api_url: str | None = None,
        konic_api_key: str | None = None,
    ):
        self.config = config
        self._konic_api_url = konic_api_url
        self._konic_api_key = konic_api_key
        self._dataset: Dataset | IterableDataset | None = None

    def load(self) -> Dataset | IterableDataset:
        if self.config.source == DatasetSource.HUGGINGFACE:
            dataset = self._load_from_huggingface()
        elif self.config.source == DatasetSource.KONIC_CLOUD:
            dataset = self._load_from_konic_cloud()
        else:
            raise KonicValidationError(
                f"Unsupported dataset source: {self.config.source}",
                field="source",
            )

        # Apply preprocessing if specified
        if self.config.preprocessing_fn:
            dataset = self._apply_preprocessing(dataset)

        # Apply max_samples limit
        if self.config.max_samples is not None and not self.config.streaming:
            dataset = dataset.select(range(min(self.config.max_samples, len(dataset))))  # type: ignore[union-attr,arg-type]

        # Shuffle if requested
        if self.config.shuffle and not self.config.streaming:
            dataset = dataset.shuffle(seed=self.config.shuffle_seed)

        self._dataset = dataset
        return dataset

    def _load_from_huggingface(self) -> Dataset | IterableDataset:
        from datasets import load_dataset

        load_kwargs = {
            "path": self.config.name,
            "split": self.config.split,
            "streaming": self.config.streaming,
        }

        if self.config.subset:
            load_kwargs["name"] = self.config.subset

        try:
            dataset = load_dataset(**load_kwargs)
            return dataset
        except Exception as e:
            raise RuntimeError(
                f"Failed to load HuggingFace dataset '{self.config.name}': {e}"
            ) from e

    def _load_from_konic_cloud(self) -> Dataset:
        import os

        import requests
        from datasets import Dataset

        # Get API credentials from environment if not provided
        api_url = self._konic_api_url or os.environ.get("KONIC_HOST")
        api_key = self._konic_api_key or os.environ.get("KONIC_API_KEY")

        if not api_url:
            raise KonicEnvironmentError(
                env_var="KONIC_HOST",
                suggestion=(
                    "Set KONIC_HOST environment variable or pass konic_api_url to DatasetLoader."
                ),
            )

        # Fetch dataset metadata and download URL
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        @_retry_with_backoff(
            max_retries=3,
            initial_delay=1.0,
            backoff_factor=2.0,
            retryable_exceptions=(requests.RequestException,),
        )
        def _fetch_dataset_info() -> dict:
            response = requests.get(
                f"{api_url}/api/data/{self.config.name}",
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

        @_retry_with_backoff(
            max_retries=3,
            initial_delay=1.0,
            backoff_factor=2.0,
            retryable_exceptions=(requests.RequestException,),
        )
        def _fetch_json_data(url: str) -> list:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()

        try:
            # Get dataset info from Konic Cloud API
            data_info = _fetch_dataset_info()

            # Download the actual data
            download_url = data_info.get("download_url")
            if not download_url:
                raise KonicValidationError(
                    f"No download URL for dataset '{self.config.name}'",
                    field="download_url",
                )

            # Load data based on format
            data_format = data_info.get("format", "json")

            if data_format == "json":
                records = _fetch_json_data(download_url)
                dataset = Dataset.from_list(records)
            elif data_format == "parquet":
                dataset = Dataset.from_parquet(download_url)
            elif data_format == "csv":
                dataset = Dataset.from_csv(download_url)
            else:
                raise KonicValidationError(
                    f"Unsupported data format: {data_format}. "
                    "Supported formats: json, parquet, csv",
                    field="format",
                )

            return dataset  # type: ignore[return-value]

        except requests.RequestException as e:
            raise RuntimeError(
                f"Failed to load Konic Cloud dataset '{self.config.name}' after retries: {e}"
            ) from e

    def _apply_preprocessing(self, dataset: Dataset | IterableDataset) -> Dataset | IterableDataset:
        fn_name = self.config.preprocessing_fn
        if fn_name not in self._preprocessing_registry:
            raise KonicValidationError(
                f"Preprocessing function '{fn_name}' not found. "
                f"Register it with @DatasetLoader.register_preprocessing",
                field="preprocessing_fn",
            )

        fn = self._preprocessing_registry[fn_name]
        return dataset.map(fn)

    @classmethod
    def register_preprocessing(cls, name: str) -> Callable:
        def decorator(fn: Callable) -> Callable:
            cls._preprocessing_registry[name] = fn
            return fn

        return decorator

    def iter_batches(
        self,
        batch_size: int = 8,
        drop_last: bool = False,
    ) -> Iterator[dict[str, list[Any]]]:
        if self._dataset is None:
            self.load()

        if self.config.streaming:
            # For streaming datasets
            yield from self._iter_streaming_batches(batch_size)
        else:
            # For regular datasets
            yield from self._iter_regular_batches(batch_size, drop_last)

    def _iter_regular_batches(
        self,
        batch_size: int,
        drop_last: bool,
    ) -> Iterator[dict[str, list[Any]]]:
        dataset_len = len(self._dataset)  # type: ignore[arg-type]
        num_batches = dataset_len // batch_size

        if not drop_last and dataset_len % batch_size != 0:
            num_batches += 1

        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, dataset_len)

            if drop_last and end_idx - start_idx < batch_size:
                break

            batch = self._dataset.select(range(start_idx, end_idx))  # type: ignore[union-attr]

            # Convert Column objects to plain Python lists for compatibility
            # with tokenizers and other libraries that expect list[str]
            yield {key: list(batch[key]) for key in batch.column_names}

    def _iter_streaming_batches(
        self,
        batch_size: int,
    ) -> Iterator[dict[str, list[Any]]]:
        batch: list[dict[str, Any]] = []
        column_names: list[str] | None = None

        for example in self._dataset:  # type: ignore[union-attr]
            batch.append(example)  # type: ignore[arg-type]
            if column_names is None:
                column_names = list(example.keys())  # type: ignore[union-attr]

            if len(batch) >= batch_size:
                yield self._batch_to_dict(batch, column_names)
                batch = []

        # Yield remaining examples
        if batch and column_names is not None:
            yield self._batch_to_dict(batch, column_names)

    def _batch_to_dict(
        self,
        batch: list[dict],
        column_names: list[str],
    ) -> dict[str, list[Any]]:
        return {key: [ex[key] for ex in batch] for key in column_names}

    def get_prompts(
        self,
        batch: dict[str, list[Any]] | None = None,
    ) -> list[str]:
        if batch is None:
            batch = next(self.iter_batches(batch_size=8))

        prompt_col = self.config.prompt_column
        if prompt_col not in batch:
            raise KeyError(
                f"Prompt column '{prompt_col}' not found in dataset. "
                f"Available columns: {list(batch.keys())}"
            )

        prompts = batch[prompt_col]

        # Convert to plain Python list if it's a HuggingFace Column or similar
        # The tokenizer expects list[str], not datasets.arrow_dataset.Column
        if not isinstance(prompts, list):
            prompts = list(prompts)

        return prompts

    @property
    def dataset(self) -> Dataset | IterableDataset:
        if self._dataset is None:
            raise RuntimeError("Dataset not loaded. Call load() first.")
        return self._dataset

    def __len__(self) -> int:
        if self._dataset is None:
            raise RuntimeError("Dataset not loaded. Call load() first.")

        if self.config.streaming:
            raise RuntimeError("Cannot get length of streaming dataset")

        return len(self._dataset)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[dict[str, Any]]:
        if self._dataset is None:
            self.load()

        yield from self._dataset  # type: ignore[misc]

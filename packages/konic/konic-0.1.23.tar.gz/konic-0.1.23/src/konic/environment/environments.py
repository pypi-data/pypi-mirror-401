"""Specialized environment implementations for Konic."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from konic.common.errors import KonicError
from konic.environment.core import (
    KonicEnvironment,
    KonicResetStateObservation,
    KonicStepStateObservation,
)
from konic.environment.reward import KonicRewardComposer
from konic.environment.space import KonicSpace
from konic.environment.termination import KonicTerminationComposer


class KonicCSVStreamerEnvironment(KonicEnvironment):
    """Environment that streams CSV data row-by-row as observations."""

    def __init__(
        self,
        csv_file_path: str | Path,
        action_space: KonicSpace,
        reward_composer: KonicRewardComposer,
        termination_composer: KonicTerminationComposer,
        flatten_spaces: bool = False,
    ):
        class EmptyObservationSpace(KonicSpace):
            pass

        super().__init__(
            action_space=action_space,
            observation_space=EmptyObservationSpace(),
            reward_composer=reward_composer,
            termination_composer=termination_composer,
            flatten_spaces=flatten_spaces,
        )

        self.csv_file_path = Path(csv_file_path)
        self._load_csv_data()

        self.current_index = 0
        self.window_buffer: list[pd.Series] = []

    def _validate_index(self, index: int) -> None:
        if index < 0 or index >= len(self.csv_df):
            raise KonicError(
                f"Row index {index} is out of bounds. Valid range: 0 to {len(self.csv_df) - 1}"
            )

    def _validate_column(self, column_name: str) -> None:
        if column_name not in self.csv_df.columns:
            raise KonicError(
                f"Column '{column_name}' not found in CSV data. "
                f"Available columns: {list(self.csv_df.columns)}"
            )

    def _load_csv_data(self) -> None:
        if not self.csv_file_path.exists():
            raise KonicError(f"CSV file not found: {self.csv_file_path}")

        try:
            self.csv_df = pd.read_csv(self.csv_file_path, dtype=str)

        except pd.errors.EmptyDataError:
            raise KonicError(f"CSV file is empty: {self.csv_file_path}")

        except Exception as e:
            raise KonicError(f"Error reading CSV file {self.csv_file_path}: {e}")

        if self.csv_df.empty:
            raise KonicError(f"CSV file contains no data rows: {self.csv_file_path}")

    def _get_current_row(self) -> pd.DataFrame:
        self._validate_index(self.current_index)
        return pd.DataFrame(self.csv_df.iloc[[self.current_index]])

    def _reset(
        self, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> KonicResetStateObservation:
        if seed is not None:
            np.random.seed(seed)

        self.current_index = 0
        observation = self.get_obs()
        info = self.get_info()

        return observation, info

    def _step(self, action: dict[str, Any]) -> KonicStepStateObservation:
        self.current_index += 1

        observation = self.get_obs()
        reward = self.reward_composer.compose()
        terminated = self.termination_composer.compose()
        truncated = self.current_index >= len(self.csv_df)
        info = self.get_info()

        return observation, reward, terminated, truncated, info

    def get_obs(self) -> pd.DataFrame:
        if self.is_done:
            return pd.DataFrame(dtype=object)
        else:
            return self._get_current_row()

    def get_info(self) -> dict[str, Any]:
        info = {
            "current_index": self.current_index,
            "total_rows": len(self.csv_df),
            "csv_file_path": str(self.csv_file_path),
            "column_names": list(self.csv_df.columns),
        }

        return info

    @property
    def is_done(self) -> bool:
        return self.current_index >= len(self.csv_df)

    @property
    def remaining_rows(self) -> int:
        return max(0, len(self.csv_df) - self.current_index)

    def get_column(self, column_name: str) -> pd.Series:
        self._validate_column(column_name)
        return self.csv_df[column_name]  # type: ignore[return-value]

    def get_current_value(self, column_name: str) -> Any:
        self._validate_index(self.current_index)
        self._validate_column(column_name)
        return self.csv_df.iloc[self.current_index][column_name]

    def get_window_values(self, column_name: str) -> list[Any]:
        self._validate_column(column_name)
        return [row[column_name] for row in self.window_buffer]

    def reset_to_row(self, row_index: int) -> KonicResetStateObservation:
        self._validate_index(row_index)
        self.current_index = row_index

        observation = self.get_obs()
        info = self.get_info()

        return observation, info

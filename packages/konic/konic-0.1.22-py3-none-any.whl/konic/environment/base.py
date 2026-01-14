from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import gymnasium as gym

if TYPE_CHECKING:
    from konic.environment.reward import KonicRewardComposer
    from konic.environment.termination import KonicTerminationComposer
    from konic.environment.type import KonicResetStateObservation, KonicStepStateObservation


class BaseKonicEnvironment(gym.Env, ABC):
    action_space: gym.spaces.Space[Any]
    observation_space: gym.spaces.Space[Any]

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def reward_composer(self) -> KonicRewardComposer:
        pass

    @property
    @abstractmethod
    def termination_composer(self) -> KonicTerminationComposer | None:
        pass

    @abstractmethod
    def step(self, action: Any) -> KonicStepStateObservation:
        pass

    @abstractmethod
    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> KonicResetStateObservation:
        pass

    @abstractmethod
    def get_obs(self) -> Any:
        pass

    @abstractmethod
    def get_info(self) -> dict:
        pass

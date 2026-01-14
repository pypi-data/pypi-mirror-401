# pyright: reportAbstractUsage=false
"""Tests for konic.callback.base module."""

from abc import ABC
from unittest.mock import MagicMock

import pytest

from konic.callback.base import BaseKonicRLCallback


class TestBaseKonicRLCallback:
    """Tests for BaseKonicRLCallback abstract class."""

    def test_is_abstract_class(self):
        assert issubclass(BaseKonicRLCallback, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError) as exc_info:
            BaseKonicRLCallback()
        assert "abstract" in str(exc_info.value).lower()

    def test_abstract_methods_exist(self):
        assert hasattr(BaseKonicRLCallback, "on_episode_start")
        assert hasattr(BaseKonicRLCallback, "on_episode_step")
        assert hasattr(BaseKonicRLCallback, "on_episode_end")
        assert hasattr(BaseKonicRLCallback, "on_train_result")

    def test_concrete_implementation(self):
        class ConcreteCallback(BaseKonicRLCallback):
            def __init__(self):
                self.calls = []

            def on_episode_start(self, *, episode, **kwargs):
                self.calls.append(("episode_start", episode))

            def on_episode_step(self, *, episode, **kwargs):
                self.calls.append(("episode_step", episode))

            def on_episode_end(self, *, episode, **kwargs):
                self.calls.append(("episode_end", episode))

            def on_train_result(self, *, algorithm, result, **kwargs):
                self.calls.append(("train_result", result))

        callback = ConcreteCallback()

        mock_episode = MagicMock()
        mock_algorithm = MagicMock()
        mock_result = {"test": "value"}

        callback.on_episode_start(episode=mock_episode)
        callback.on_episode_step(episode=mock_episode)
        callback.on_episode_end(episode=mock_episode)
        callback.on_train_result(algorithm=mock_algorithm, result=mock_result)

        assert len(callback.calls) == 4
        assert callback.calls[0] == ("episode_start", mock_episode)
        assert callback.calls[1] == ("episode_step", mock_episode)
        assert callback.calls[2] == ("episode_end", mock_episode)
        assert callback.calls[3] == ("train_result", mock_result)

    def test_partial_implementation_fails(self):
        class PartialCallback(BaseKonicRLCallback):
            def on_episode_start(self, *, episode, **kwargs):
                pass

            def on_episode_step(self, *, episode, **kwargs):
                pass

            # Missing on_episode_end and on_train_result

        with pytest.raises(TypeError):
            PartialCallback()

    def test_accepts_kwargs(self):
        class KwargsCallback(BaseKonicRLCallback):
            def __init__(self):
                self.kwargs_received = []

            def on_episode_start(self, *, episode, **kwargs):
                self.kwargs_received.append(kwargs)

            def on_episode_step(self, *, episode, **kwargs):
                self.kwargs_received.append(kwargs)

            def on_episode_end(self, *, episode, **kwargs):
                self.kwargs_received.append(kwargs)

            def on_train_result(self, *, algorithm, result, **kwargs):
                self.kwargs_received.append(kwargs)

        callback = KwargsCallback()
        mock_episode = MagicMock()

        callback.on_episode_start(episode=mock_episode, extra_arg="value")
        assert callback.kwargs_received[-1] == {"extra_arg": "value"}

        callback.on_train_result(
            algorithm=MagicMock(),
            result={},
            custom="data",
            another=123,
        )
        assert callback.kwargs_received[-1] == {"custom": "data", "another": 123}

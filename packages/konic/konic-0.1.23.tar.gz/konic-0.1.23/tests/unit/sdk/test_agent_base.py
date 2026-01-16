# pyright: reportAbstractUsage=false
"""Tests for konic.agent.base module."""

from abc import ABC
from unittest.mock import MagicMock

import pytest

from konic.agent.base import BaseKonicAgent


class TestBaseKonicAgent:
    """Tests for BaseKonicAgent abstract class."""

    def test_is_abstract_class(self):
        assert issubclass(BaseKonicAgent, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError) as exc_info:
            BaseKonicAgent()
        assert "abstract" in str(exc_info.value).lower()

    def test_abstract_methods_exist(self):
        assert hasattr(BaseKonicAgent, "get_environment")
        assert hasattr(BaseKonicAgent, "get_environment_config")
        assert hasattr(BaseKonicAgent, "get_algorithm_config")
        assert hasattr(BaseKonicAgent, "get_module")
        assert hasattr(BaseKonicAgent, "get_training_config")

    def test_concrete_implementation(self):
        class ConcreteAgent(BaseKonicAgent):
            def get_environment(self):
                return MagicMock()

            def get_environment_config(self):
                return {"key": "value"}

            def get_algorithm_config(self):
                return {"algorithm": "ppo"}

            def get_module(self):
                return None

            def get_training_config(self):
                return {"iterations": 100}

        agent = ConcreteAgent()

        assert agent.get_environment_config() == {"key": "value"}
        assert agent.get_algorithm_config() == {"algorithm": "ppo"}
        assert agent.get_module() is None
        assert agent.get_training_config() == {"iterations": 100}

    def test_partial_implementation_fails(self):
        class PartialAgent(BaseKonicAgent):
            def get_environment(self):
                return MagicMock()

            def get_environment_config(self):
                return {}

            # Missing other methods

        with pytest.raises(TypeError):
            PartialAgent()

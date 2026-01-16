"""Tests for TRL backend implementations."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from konic.common.errors import KonicConfigurationError, KonicValidationError
from konic.finetuning.backends.base import BackendConfig
from konic.finetuning.backends.result import FinetuningResult
from konic.finetuning.config import GenerationConfig, TrainingConfig


@pytest.fixture
def mock_trl_module():
    """Create a mock TRL module for testing."""
    mock_trl = MagicMock()
    mock_trl.GRPOConfig = MagicMock()
    mock_trl.DPOConfig = MagicMock()
    mock_trl.GRPOTrainer = MagicMock()
    mock_trl.DPOTrainer = MagicMock()
    return mock_trl


@pytest.fixture
def mock_backend_config():
    """Create a mock backend config for testing."""
    mock_reward_composer = MagicMock()
    mock_reward_composer.compose_batch.return_value = ([0.5, 0.6], {"reward": [0.5, 0.6]})

    mock_dataset_config = MagicMock()
    mock_dataset_config.name = "test_dataset"
    mock_dataset_config.prompt_column = "prompt"

    mock_callback = MagicMock()

    return BackendConfig(
        model_name="gpt2",
        reward_composer=mock_reward_composer,
        dataset_config=mock_dataset_config,
        lora_config=None,
        training_config=TrainingConfig(),
        generation_config=GenerationConfig(),
        callback=mock_callback,
        checkpoint_dir=None,
        device="cpu",
    )


class TestCheckTRLAvailable:
    """Tests for check_trl_available function."""

    def test_returns_true_when_trl_installed(self):
        """Test that check_trl_available returns True when TRL is installed."""
        # Reset cached value
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = None

        with patch.dict(sys.modules, {"trl": MagicMock()}):
            from konic.finetuning.backends.trl.base import check_trl_available

            # Reset again after import
            trl_base._TRL_AVAILABLE = None
            result = check_trl_available()
            assert result is True

    def test_returns_false_when_trl_not_installed(self):
        """Test that check_trl_available returns False when TRL is not installed."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = None

        with patch.dict(sys.modules, {"trl": None}):
            # Force reimport
            trl_base._TRL_AVAILABLE = None
            with patch("builtins.__import__", side_effect=ImportError("No module named 'trl'")):
                result = trl_base.check_trl_available()
                assert result is False

    def test_caches_result(self):
        """Test that check_trl_available caches the result."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True
        result = trl_base.check_trl_available()
        assert result is True


class TestRequireTRL:
    """Tests for require_trl function."""

    def test_raises_when_trl_not_available(self):
        """Test that require_trl raises error when TRL is not available."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = False

        with pytest.raises(KonicConfigurationError) as exc_info:
            trl_base.require_trl()

        assert "trl" in str(exc_info.value).lower()

    def test_passes_when_trl_available(self):
        """Test that require_trl passes when TRL is available."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True
        # Should not raise
        trl_base.require_trl()


class TestBaseTRLBackend:
    """Tests for BaseTRLBackend abstract class."""

    def test_init_requires_trl(self):
        """Test that BaseTRLBackend.__init__ requires TRL."""
        import konic.finetuning.backends.trl.base as trl_base

        # Save original value
        original = trl_base._TRL_AVAILABLE
        trl_base._TRL_AVAILABLE = False

        try:
            # Create a concrete subclass to test
            class TestBackend(trl_base.BaseTRLBackend):
                def _validate_config(self):
                    pass

                def _create_trainer(self):
                    pass

                def train(self, max_iterations, save_every=None):
                    return FinetuningResult(total_iterations=0)

            with pytest.raises(KonicConfigurationError):
                TestBackend()
        finally:
            # Restore original value
            trl_base._TRL_AVAILABLE = original

    def test_config_property_raises_before_setup(self):
        """Test that config property raises before setup."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        # Create a concrete subclass for testing
        class TestBackend(trl_base.BaseTRLBackend):
            def _validate_config(self):
                pass

            def _create_trainer(self):
                pass

            def train(self, max_iterations, save_every=None):
                return FinetuningResult(total_iterations=0)

        backend = TestBackend()
        with pytest.raises(KonicConfigurationError):
            _ = backend.config

    def test_is_setup_property(self):
        """Test is_setup property."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        class TestBackend(trl_base.BaseTRLBackend):
            def _validate_config(self):
                pass

            def _create_trainer(self):
                pass

            def train(self, max_iterations, save_every=None):
                return FinetuningResult(total_iterations=0)

        backend = TestBackend()
        assert backend.is_setup is False

    def test_setup_calls_validate_and_create_trainer(self, mock_backend_config):
        """Test that setup calls validation and trainer creation."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        class TestBackend(trl_base.BaseTRLBackend):
            def __init__(self):
                super().__init__()
                self.validate_called = False
                self.create_trainer_called = False

            def _validate_config(self):
                self.validate_called = True

            def _create_trainer(self):
                self.create_trainer_called = True

            def train(self, max_iterations, save_every=None):
                return FinetuningResult(total_iterations=0)

        backend = TestBackend()
        backend.setup(mock_backend_config)

        assert backend.validate_called is True
        assert backend.create_trainer_called is True
        assert backend.is_setup is True

    def test_setup_skips_if_already_setup(self, mock_backend_config):
        """Test that setup skips if already setup."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        call_count = 0

        class TestBackend(trl_base.BaseTRLBackend):
            def _validate_config(self):
                nonlocal call_count
                call_count += 1

            def _create_trainer(self):
                pass

            def train(self, max_iterations, save_every=None):
                return FinetuningResult(total_iterations=0)

        backend = TestBackend()
        backend.setup(mock_backend_config)
        backend.setup(mock_backend_config)

        assert call_count == 1

    def test_evaluate_raises_without_trainer(self, mock_backend_config):
        """Test that evaluate raises when trainer is not initialized."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        class TestBackend(trl_base.BaseTRLBackend):
            def _validate_config(self):
                pass

            def _create_trainer(self):
                # Don't set _trainer
                pass

            def train(self, max_iterations, save_every=None):
                return FinetuningResult(total_iterations=0)

        backend = TestBackend()
        backend.setup(mock_backend_config)

        with pytest.raises(KonicConfigurationError):
            backend.evaluate(["test prompt"])


class TestTRLModuleExports:
    """Tests for TRL module exports and lazy imports."""

    def test_get_trl_grpo_backend(self):
        """Test get_trl_grpo_backend lazy import."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl import get_trl_grpo_backend

        backend_cls = get_trl_grpo_backend()
        assert backend_cls.__name__ == "TRLGRPOBackend"

    def test_get_trl_dpo_backend(self):
        """Test get_trl_dpo_backend lazy import."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl import get_trl_dpo_backend

        backend_cls = get_trl_dpo_backend()
        assert backend_cls.__name__ == "TRLDPOBackend"


class TestTRLGRPOBackend:
    """Tests for TRLGRPOBackend."""

    def test_name_property(self):
        """Test GRPO backend name property."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.grpo import TRLGRPOBackend

        backend = TRLGRPOBackend()
        assert backend.name == "TRLGRPOBackend"

    def test_validate_config_requires_reward_composer(self, mock_backend_config):
        """Test that GRPO backend requires reward_composer."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.grpo import TRLGRPOBackend

        # Config without reward composer
        mock_backend_config.reward_composer = None

        backend = TRLGRPOBackend()
        backend._config = mock_backend_config

        with pytest.raises(KonicValidationError) as exc_info:
            backend._validate_config()

        assert "reward_composer" in str(exc_info.value)


class TestTRLDPOBackend:
    """Tests for TRLDPOBackend."""

    def test_name_property(self):
        """Test DPO backend name property."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.dpo import TRLDPOBackend

        backend = TRLDPOBackend()
        assert backend.name == "TRLDPOBackend"

    def test_validate_config_requires_preference_columns(self, mock_backend_config):
        """Test that DPO backend requires preference columns in dataset."""
        import konic.finetuning.backends.trl.base as trl_base

        trl_base._TRL_AVAILABLE = True

        from konic.finetuning.backends.trl.dpo import TRLDPOBackend

        # Config without preference columns
        mock_backend_config.dataset_config.chosen_column = None
        mock_backend_config.dataset_config.rejected_column = None

        backend = TRLDPOBackend()
        backend._config = mock_backend_config

        with pytest.raises(KonicValidationError) as exc_info:
            backend._validate_config()

        assert "preference" in str(exc_info.value).lower() or "dpo" in str(exc_info.value).lower()

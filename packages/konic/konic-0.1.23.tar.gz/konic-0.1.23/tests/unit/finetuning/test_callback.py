# pyright: reportArgumentType=false
"""Tests for konic.finetuning.callback module."""

from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest

from konic.finetuning.callback import (
    BaseKonicFinetuningCallback,
    CompositeCallback,
    KonicFinetuningCallback,
)


@dataclass
class MockFinetuningIterationResult:
    """Mock result for testing callbacks."""

    iteration: int = 1
    reward_mean: float = 0.5
    reward_std: float = 0.1
    kl_divergence: float = 0.05
    policy_loss: float = 0.1
    value_loss: float = 0.05
    total_loss: float = 0.15
    total_time_sec: float = 1.0

    def to_dict(self):
        return {
            "iteration": self.iteration,
            "reward_mean": self.reward_mean,
            "kl_divergence": self.kl_divergence,
            "total_loss": self.total_loss,
        }


@dataclass
class MockFinetuningResult:
    """Mock result for testing callbacks."""

    final_reward_mean: float = 0.8
    best_reward: float = 0.9
    best_iteration: int = 50
    total_time_sec: float = 120.0

    def summary(self):
        return "Mock Summary"


class TestBaseKonicFinetuningCallback:
    """Tests for BaseKonicFinetuningCallback abstract class."""

    def test_default_methods_do_nothing(self):
        class ConcreteCallback(BaseKonicFinetuningCallback):
            pass

        callback = ConcreteCallback()

        # All these should be no-ops
        callback.on_train_begin({"test": "config"})
        callback.on_train_end(MockFinetuningResult())
        callback.on_iteration_begin(1)
        callback.on_iteration_end(MockFinetuningIterationResult())
        callback.on_generation_begin(["prompt"])
        callback.on_generation_end(["prompt"], ["response"])
        callback.on_reward_computed([0.5], {"reward": [0.5]})
        callback.on_checkpoint_saved("/path", 1)

    def test_should_stop_early_default(self):
        class ConcreteCallback(BaseKonicFinetuningCallback):
            pass

        callback = ConcreteCallback()
        result = callback.should_stop_early(MockFinetuningIterationResult())
        assert result is False


class TestKonicFinetuningCallback:
    """Tests for KonicFinetuningCallback class."""

    def test_init_defaults(self):
        callback = KonicFinetuningCallback()

        assert callback.log_interval == 1
        assert callback.log_samples is False
        assert callback.max_samples_to_log == 3
        assert callback.use_mlflow is True
        assert callback.early_stop_kl_threshold is None
        assert callback.early_stop_patience == 5
        assert callback.verbose is True
        assert callback._high_kl_count == 0
        assert callback._mlflow_initialized is False

    def test_init_custom_values(self):
        callback = KonicFinetuningCallback(
            log_interval=5,
            log_samples=True,
            max_samples_to_log=10,
            use_mlflow=False,
            early_stop_kl_threshold=0.1,
            early_stop_patience=3,
            verbose=False,
        )

        assert callback.log_interval == 5
        assert callback.log_samples is True
        assert callback.max_samples_to_log == 10
        assert callback.use_mlflow is False
        assert callback.early_stop_kl_threshold == 0.1
        assert callback.early_stop_patience == 3
        assert callback.verbose is False

    def test_on_train_begin_verbose(self, capsys):
        callback = KonicFinetuningCallback(use_mlflow=False, verbose=True)
        config = {
            "model_name": "test-model",
            "use_lora": True,
            "learning_rate": 1e-5,
            "batch_size": 8,
            "max_iterations": 100,
        }

        callback.on_train_begin(config)

        captured = capsys.readouterr()
        assert "Starting RLHF Training" in captured.out
        assert "test-model" in captured.out
        assert "True" in captured.out  # use_lora

    def test_on_train_begin_not_verbose(self, capsys):
        callback = KonicFinetuningCallback(use_mlflow=False, verbose=False)
        callback.on_train_begin({"model_name": "test"})

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_on_train_begin_with_mlflow(self):
        # Test that mlflow initialization is attempted
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        config = {"model_name": "test", "batch_size": 8}

        # This will attempt to use mlflow - if not installed, it will disable it
        callback.on_train_begin(config)

        # Either mlflow was initialized successfully, or was disabled due to import error
        assert callback._mlflow_initialized or not callback.use_mlflow

    def test_on_train_begin_mlflow_import_error(self):
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)

        # Simulate the scenario where _init_mlflow would handle import error
        # The actual method handles this gracefully by setting use_mlflow to False
        callback.on_train_begin({})
        # If mlflow is not installed, it should be disabled
        # No assertion needed - just verify no exception is raised

    def test_on_train_end_verbose(self, capsys):
        callback = KonicFinetuningCallback(use_mlflow=False, verbose=True)
        result = MockFinetuningResult()

        callback.on_train_end(result)

        captured = capsys.readouterr()
        assert "Mock Summary" in captured.out

    def test_on_train_end_not_verbose(self, capsys):
        callback = KonicFinetuningCallback(use_mlflow=False, verbose=False)
        result = MockFinetuningResult()

        callback.on_train_end(result)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_on_train_end_with_mlflow_initialized(self):
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        callback._mlflow_initialized = True
        callback.use_mlflow = True
        result = MockFinetuningResult()

        # Even if mlflow is not installed, this should not raise
        try:
            callback.on_train_end(result)
        except ImportError:
            # mlflow not installed - this is expected in test environment
            pass

    def test_on_iteration_end_logs_at_interval(self, capsys):
        callback = KonicFinetuningCallback(log_interval=2, use_mlflow=False, verbose=True)

        # Iteration 1 - should not log (not divisible by 2)
        callback.on_iteration_end(MockFinetuningIterationResult(iteration=1))
        captured = capsys.readouterr()
        assert "[Iter" not in captured.out

        # Iteration 2 - should log
        callback.on_iteration_end(MockFinetuningIterationResult(iteration=2))
        captured = capsys.readouterr()
        assert "Iter" in captured.out and "2" in captured.out

    def test_on_generation_end_stores_samples(self):
        callback = KonicFinetuningCallback(log_samples=True, max_samples_to_log=2)

        prompts = ["p1", "p2", "p3"]
        responses = ["r1", "r2", "r3"]

        callback.on_generation_end(prompts, responses)

        assert callback._current_prompts == ["p1", "p2"]
        assert callback._current_responses == ["r1", "r2"]

    def test_should_stop_early_no_threshold(self):
        callback = KonicFinetuningCallback(early_stop_kl_threshold=None)
        result = MockFinetuningIterationResult(kl_divergence=1.0)

        assert callback.should_stop_early(result) is False

    def test_should_stop_early_below_threshold(self):
        callback = KonicFinetuningCallback(early_stop_kl_threshold=0.1)
        result = MockFinetuningIterationResult(kl_divergence=0.05)

        assert callback.should_stop_early(result) is False
        assert callback._high_kl_count == 0

    def test_should_stop_early_above_threshold_resets(self, capsys):
        callback = KonicFinetuningCallback(
            early_stop_kl_threshold=0.1, early_stop_patience=3, verbose=True
        )

        # Build up count
        callback.should_stop_early(MockFinetuningIterationResult(kl_divergence=0.15))
        assert callback._high_kl_count == 1

        callback.should_stop_early(MockFinetuningIterationResult(kl_divergence=0.15))
        assert callback._high_kl_count == 2

        # Reset with good result
        callback.should_stop_early(MockFinetuningIterationResult(kl_divergence=0.05))
        assert callback._high_kl_count == 0

    def test_should_stop_early_triggers(self, capsys):
        callback = KonicFinetuningCallback(
            early_stop_kl_threshold=0.1, early_stop_patience=2, verbose=True
        )

        callback.should_stop_early(MockFinetuningIterationResult(kl_divergence=0.15))
        assert callback._high_kl_count == 1

        result = callback.should_stop_early(MockFinetuningIterationResult(kl_divergence=0.15))
        assert result is True
        assert callback._high_kl_count == 2

        captured = capsys.readouterr()
        assert "Early stopping triggered" in captured.out

    def test_on_checkpoint_saved_verbose(self, capsys):
        callback = KonicFinetuningCallback(use_mlflow=False, verbose=True)

        callback.on_checkpoint_saved("/path/to/checkpoint", 10)

        captured = capsys.readouterr()
        assert "Checkpoint saved" in captured.out
        assert "/path/to/checkpoint" in captured.out
        assert "10" in captured.out

    def test_on_checkpoint_saved_with_mlflow_initialized(self):
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        callback._mlflow_initialized = True
        callback.use_mlflow = True

        # Should not raise even if mlflow is not installed
        try:
            callback.on_checkpoint_saved("/path/to/checkpoint", 10)
        except ImportError:
            # mlflow not installed - acceptable
            pass

    def test_log_iteration_console(self, capsys):
        callback = KonicFinetuningCallback(use_mlflow=False, verbose=True)
        result = MockFinetuningIterationResult(
            iteration=5,
            reward_mean=0.75,
            reward_std=0.1,
            kl_divergence=0.03,
            total_loss=0.15,
        )

        callback._log_iteration_console(result)

        captured = capsys.readouterr()
        assert "Iter" in captured.out and "5" in captured.out
        assert "0.75" in captured.out or "0.7" in captured.out

    def test_log_iteration_mlflow_initialized(self):
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        result = MockFinetuningIterationResult(iteration=5)

        # Should not raise even if mlflow is not installed
        try:
            callback._log_iteration_mlflow(result)
        except ImportError:
            # mlflow not installed - acceptable
            pass

    def test_log_samples(self, capsys):
        callback = KonicFinetuningCallback(
            log_samples=True, max_samples_to_log=2, verbose=True, use_mlflow=False
        )
        callback._current_prompts = ["prompt1", "prompt2"]
        callback._current_responses = ["response1", "response2"]

        callback._log_samples(5)

        captured = capsys.readouterr()
        assert "Sample Generations" in captured.out
        assert "prompt1" in captured.out
        assert "response1" in captured.out

        # Should clear stored samples
        assert callback._current_prompts == []
        assert callback._current_responses == []


class TestCompositeCallback:
    """Tests for CompositeCallback class."""

    def test_init(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)

        composite = CompositeCallback([cb1, cb2])

        assert len(composite.callbacks) == 2
        assert cb1 in composite.callbacks
        assert cb2 in composite.callbacks

    def test_on_train_begin_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        config = {"test": "config"}
        composite.on_train_begin(config)

        cb1.on_train_begin.assert_called_once_with(config)
        cb2.on_train_begin.assert_called_once_with(config)

    def test_on_train_end_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        result = MockFinetuningResult()
        composite.on_train_end(result)

        cb1.on_train_end.assert_called_once_with(result)
        cb2.on_train_end.assert_called_once_with(result)

    def test_on_iteration_begin_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        composite.on_iteration_begin(5)

        cb1.on_iteration_begin.assert_called_once_with(5)
        cb2.on_iteration_begin.assert_called_once_with(5)

    def test_on_iteration_end_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        result = MockFinetuningIterationResult()
        composite.on_iteration_end(result)

        cb1.on_iteration_end.assert_called_once_with(result)
        cb2.on_iteration_end.assert_called_once_with(result)

    def test_on_generation_begin_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        prompts = ["p1", "p2"]
        composite.on_generation_begin(prompts)

        cb1.on_generation_begin.assert_called_once_with(prompts)
        cb2.on_generation_begin.assert_called_once_with(prompts)

    def test_on_generation_end_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        prompts = ["p1"]
        responses = ["r1"]
        composite.on_generation_end(prompts, responses)

        cb1.on_generation_end.assert_called_once_with(prompts, responses)
        cb2.on_generation_end.assert_called_once_with(prompts, responses)

    def test_on_reward_computed_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        rewards = [0.5]
        breakdown = {"r": [0.5]}
        composite.on_reward_computed(rewards, breakdown)

        cb1.on_reward_computed.assert_called_once_with(rewards, breakdown)
        cb2.on_reward_computed.assert_called_once_with(rewards, breakdown)

    def test_on_checkpoint_saved_calls_all(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        composite = CompositeCallback([cb1, cb2])

        composite.on_checkpoint_saved("/path", 10)

        cb1.on_checkpoint_saved.assert_called_once_with("/path", 10)
        cb2.on_checkpoint_saved.assert_called_once_with("/path", 10)

    def test_should_stop_early_any_true(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb1.should_stop_early.return_value = False
        cb2.should_stop_early.return_value = True
        composite = CompositeCallback([cb1, cb2])

        result = MockFinetuningIterationResult()
        assert composite.should_stop_early(result) is True

    def test_should_stop_early_all_false(self):
        cb1 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb2 = MagicMock(spec=BaseKonicFinetuningCallback)
        cb1.should_stop_early.return_value = False
        cb2.should_stop_early.return_value = False
        composite = CompositeCallback([cb1, cb2])

        result = MockFinetuningIterationResult()
        assert composite.should_stop_early(result) is False

    def test_empty_callbacks(self):
        composite = CompositeCallback([])

        # Should not raise
        composite.on_train_begin({})
        composite.on_iteration_end(MockFinetuningIterationResult())
        assert composite.should_stop_early(MockFinetuningIterationResult()) is False


class TestKonicFinetuningCallbackMLflow:
    """Tests for MLflow integration in KonicFinetuningCallback."""

    @pytest.fixture
    def mock_mlflow(self):
        """Fixture to mock mlflow module."""
        mock = MagicMock()
        return mock

    def test_on_train_end_with_mlflow_logs_metrics(self, mock_mlflow):
        """Test that on_train_end logs final metrics to MLflow."""
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        callback._mlflow_initialized = True
        result = MockFinetuningResult()

        with patch.dict("sys.modules", {"mlflow": mock_mlflow}):
            callback.on_train_end(result)

            # Verify all final metrics are logged
            calls = mock_mlflow.log_metric.call_args_list
            metric_names = [c[0][0] for c in calls]

            assert "final/reward_mean" in metric_names
            assert "final/best_reward" in metric_names
            assert "final/best_iteration" in metric_names
            assert "final/total_time_sec" in metric_names

    def test_on_iteration_end_logs_samples_when_enabled(self, capsys):
        """Test that on_iteration_end logs samples when log_samples is True."""
        callback = KonicFinetuningCallback(
            log_samples=True, log_interval=1, use_mlflow=False, verbose=True
        )
        callback._current_prompts = ["test prompt"]
        callback._current_responses = ["test response"]

        result = MockFinetuningIterationResult(iteration=1)
        callback.on_iteration_end(result)

        captured = capsys.readouterr()
        assert "Sample Generations" in captured.out

        # Samples should be cleared after logging
        assert callback._current_prompts == []
        assert callback._current_responses == []

    def test_on_iteration_end_with_mlflow_logs_metrics(self, mock_mlflow):
        """Test that on_iteration_end logs iteration metrics to MLflow."""
        callback = KonicFinetuningCallback(use_mlflow=True, log_interval=1, verbose=False)
        callback._mlflow_initialized = True

        result = MockFinetuningIterationResult(iteration=5)

        with patch.dict("sys.modules", {"mlflow": mock_mlflow}):
            callback.on_iteration_end(result)

            # Verify metrics are logged with correct step
            calls = mock_mlflow.log_metric.call_args_list
            assert len(calls) > 0

            # All calls should have step=5
            for call in calls:
                assert call[1]["step"] == 5

    def test_log_iteration_mlflow_skips_non_numeric_and_iteration(self, mock_mlflow):
        """Test that _log_iteration_mlflow handles non-numeric values correctly."""
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)

        @dataclass
        class ResultWithMixedTypes:
            iteration: int = 1
            reward_mean: float = 0.5
            extra_string: str = "not logged"

            def to_dict(self):
                return {
                    "iteration": self.iteration,
                    "reward_mean": self.reward_mean,
                    "extra_string": self.extra_string,
                }

        result = ResultWithMixedTypes()

        with patch.dict("sys.modules", {"mlflow": mock_mlflow}):
            callback._log_iteration_mlflow(result)

            # Should only log numeric values, not 'iteration' or strings
            calls = mock_mlflow.log_metric.call_args_list
            logged_keys = [c[0][0] for c in calls]

            assert "reward_mean" in logged_keys
            assert "iteration" not in logged_keys
            assert "extra_string" not in logged_keys

    def test_on_checkpoint_saved_with_mlflow_logs_artifact(self, mock_mlflow):
        """Test that on_checkpoint_saved logs artifact to MLflow."""
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        callback._mlflow_initialized = True

        with patch.dict("sys.modules", {"mlflow": mock_mlflow}):
            callback.on_checkpoint_saved("/path/to/checkpoint", 10)

            mock_mlflow.log_artifact.assert_called_once_with("/path/to/checkpoint")

    def test_init_mlflow_logs_params(self, mock_mlflow):
        """Test that _init_mlflow logs config params to MLflow."""
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)
        config = {
            "model_name": "test-model",
            "batch_size": 8,
            "learning_rate": 1e-5,
            "use_lora": True,
            "complex_object": {"nested": "value"},  # Should be skipped
        }

        with patch.dict("sys.modules", {"mlflow": mock_mlflow}):
            callback._init_mlflow(config)

            # Verify params are logged
            calls = mock_mlflow.log_param.call_args_list
            logged_keys = [c[0][0] for c in calls]

            assert "model_name" in logged_keys
            assert "batch_size" in logged_keys
            assert "learning_rate" in logged_keys
            assert "use_lora" in logged_keys
            assert "complex_object" not in logged_keys

            assert callback._mlflow_initialized is True

    def test_init_mlflow_handles_import_error(self):
        """Test that _init_mlflow handles ImportError gracefully."""
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)

        # Simulate import error by removing mlflow from modules
        with patch.dict("sys.modules", {"mlflow": None}):
            # Force import error
            original_import = __builtins__["__import__"]

            def import_error_on_mlflow(name, *args, **kwargs):
                if name == "mlflow":
                    raise ImportError("No module named 'mlflow'")
                return original_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=import_error_on_mlflow):
                callback._init_mlflow({})

        # After failure, use_mlflow should be disabled
        assert callback._mlflow_initialized is False

    def test_init_mlflow_handles_generic_exception(self, mock_mlflow):
        """Test that _init_mlflow handles generic exceptions gracefully."""
        callback = KonicFinetuningCallback(use_mlflow=True, verbose=False)

        mock_mlflow.log_param.side_effect = RuntimeError("MLflow error")

        with patch.dict("sys.modules", {"mlflow": mock_mlflow}):
            callback._init_mlflow({"test": "value"})

        assert callback.use_mlflow is False
        assert callback._mlflow_initialized is False

    def test_on_iteration_end_no_samples_when_prompts_empty(self, capsys):
        """Test that on_iteration_end doesn't log samples when prompts are empty."""
        callback = KonicFinetuningCallback(
            log_samples=True, log_interval=1, use_mlflow=False, verbose=True
        )
        callback._current_prompts = []  # Empty

        result = MockFinetuningIterationResult(iteration=1)
        callback.on_iteration_end(result)

        captured = capsys.readouterr()
        assert "Sample Generations" not in captured.out

    def test_should_stop_early_verbose_warning(self, capsys):
        """Test that should_stop_early logs warning when KL is high."""
        callback = KonicFinetuningCallback(
            early_stop_kl_threshold=0.1, early_stop_patience=5, verbose=True
        )

        result = MockFinetuningIterationResult(kl_divergence=0.15)
        callback.should_stop_early(result)

        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "KL divergence" in captured.out
        assert "0.15" in captured.out or "0.1500" in captured.out

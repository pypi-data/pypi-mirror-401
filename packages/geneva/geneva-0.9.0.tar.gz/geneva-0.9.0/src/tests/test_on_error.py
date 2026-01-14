# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the simplified on_error UDF API"""

import logging
from pathlib import Path

import lance
import pyarrow as pa
import pytest

import geneva
from geneva import (
    Fail,
    Retry,
    Skip,
    fail_fast,
    retry_all,
    retry_transient,
    skip_on_error,
    udf,
)
from geneva.db import Connection
from geneva.debug.error_store import (
    ErrorHandlingConfig,
    ExceptionMatcher,
    FaultIsolation,
    Outcome,
    get_exception_outcome,
    resolve_on_error,
)

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 20

pytestmark = pytest.mark.ray


# =============================================================================
# Unit tests for ExceptionMatcher classes
# =============================================================================


class TestExceptionMatcher:
    """Tests for the ExceptionMatcher base class and matching logic"""

    def test_matches_exception_type(self) -> None:
        """Test matching by exception type"""
        matcher = ExceptionMatcher(exceptions=(ValueError,))
        assert matcher.matches(ValueError("test"))
        assert not matcher.matches(TypeError("test"))

    def test_matches_multiple_exception_types(self) -> None:
        """Test matching multiple exception types"""
        matcher = ExceptionMatcher(exceptions=(ValueError, TypeError))
        assert matcher.matches(ValueError("test"))
        assert matcher.matches(TypeError("test"))
        assert not matcher.matches(KeyError("test"))

    def test_matches_exception_subclass(self) -> None:
        """Test that exception inheritance is respected"""
        matcher = ExceptionMatcher(exceptions=(OSError,))
        assert matcher.matches(OSError("test"))
        assert matcher.matches(ConnectionError("test"))  # subclass of OSError
        assert not matcher.matches(ValueError("test"))

    def test_match_substring(self) -> None:
        """Test substring matching (plain string as regex)"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match="rate limit")
        assert matcher.matches(ValueError("rate limit exceeded"))
        assert matcher.matches(ValueError("hit rate limit"))
        assert not matcher.matches(ValueError("Rate Limit"))  # case-sensitive
        assert not matcher.matches(ValueError("invalid input"))

    def test_match_case_insensitive(self) -> None:
        """Test case-insensitive matching with (?i) flag"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match=r"(?i)rate limit")
        assert matcher.matches(ValueError("Rate limit exceeded"))
        assert matcher.matches(ValueError("RATE LIMIT hit"))
        assert not matcher.matches(ValueError("invalid input"))

    def test_match_regex(self) -> None:
        """Test regex pattern matching"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match=r"rate.?limit")
        assert matcher.matches(ValueError("rate limit"))
        assert matcher.matches(ValueError("ratelimit"))
        assert matcher.matches(ValueError("rate_limit"))
        assert not matcher.matches(ValueError("RATE_LIMIT"))  # case-sensitive
        assert not matcher.matches(ValueError("invalid"))

    def test_match_regex_alternation(self) -> None:
        """Test regex with alternation"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match=r"429|rate.?limit")
        assert matcher.matches(ValueError("Error 429"))
        assert matcher.matches(ValueError("rate limit exceeded"))
        assert not matcher.matches(ValueError("invalid input"))

    def test_invalid_regex_raises_error(self) -> None:
        """Test that invalid regex pattern raises ValueError at construction time"""
        with pytest.raises(ValueError, match="Invalid regex pattern"):
            ExceptionMatcher(exceptions=(ValueError,), match=r"[invalid")

    def test_invalid_regex_in_retry_raises_error(self) -> None:
        """Test that invalid regex in Retry raises ValueError"""
        with pytest.raises(ValueError, match="Invalid regex pattern"):
            Retry(ValueError, match=r"(unclosed group")


class TestRetryClass:
    """Tests for the Retry matcher class"""

    def test_retry_single_exception(self) -> None:
        """Test Retry with a single exception type"""
        retry = Retry(ConnectionError)
        assert retry.exceptions == (ConnectionError,)
        assert retry.max_attempts == 3
        assert retry.backoff == "exponential"

    def test_retry_multiple_exceptions(self) -> None:
        """Test Retry with multiple exception types"""
        retry = Retry(ConnectionError, TimeoutError, max_attempts=5)
        assert retry.exceptions == (ConnectionError, TimeoutError)
        assert retry.max_attempts == 5

    def test_retry_with_match(self) -> None:
        """Test Retry with match pattern"""
        retry = Retry(ValueError, match="rate limit", max_attempts=10)
        assert retry.matches(ValueError("rate limit exceeded"))
        assert not retry.matches(ValueError("invalid input"))
        assert retry.max_attempts == 10

    def test_retry_custom_backoff(self) -> None:
        """Test Retry with custom backoff strategy"""
        retry = Retry(ValueError, backoff="fixed")
        assert retry.backoff == "fixed"

    def test_retry_invalid_backoff_raises_error(self) -> None:
        """Test that invalid backoff strategy raises ValueError"""
        with pytest.raises(ValueError, match="Invalid backoff strategy"):
            Retry(ValueError, backoff="invalid_strategy")

    def test_retry_all_valid_backoff_strategies(self) -> None:
        """Test all valid backoff strategies"""
        for strategy in ["exponential", "fixed", "linear"]:
            retry = Retry(ValueError, backoff=strategy)
            assert retry.backoff == strategy


class TestSkipClass:
    """Tests for the Skip matcher class"""

    def test_skip_single_exception(self) -> None:
        """Test Skip with a single exception type"""
        skip = Skip(ValueError)
        assert skip.exceptions == (ValueError,)
        assert skip.matches(ValueError("test"))

    def test_skip_multiple_exceptions(self) -> None:
        """Test Skip with multiple exception types"""
        skip = Skip(ValueError, KeyError)
        assert skip.exceptions == (ValueError, KeyError)
        assert skip.matches(ValueError("test"))
        assert skip.matches(KeyError("test"))

    def test_skip_with_match(self) -> None:
        """Test Skip with match pattern"""
        skip = Skip(ValueError, match="invalid input")
        assert skip.matches(ValueError("invalid input provided"))
        assert not skip.matches(ValueError("rate limit exceeded"))


class TestFailClass:
    """Tests for the Fail matcher class"""

    def test_fail_single_exception(self) -> None:
        """Test Fail with a single exception type"""
        fail = Fail(RuntimeError)
        assert fail.exceptions == (RuntimeError,)
        assert fail.matches(RuntimeError("fatal error"))

    def test_fail_with_match(self) -> None:
        """Test Fail with match pattern"""
        fail = Fail(ValueError, match="fatal")
        assert fail.matches(ValueError("fatal error occurred"))
        assert not fail.matches(ValueError("minor issue"))


# =============================================================================
# Unit tests for resolve_on_error and presets
# =============================================================================


class TestFactoryFunctions:
    """Tests for factory function configurations"""

    def test_retry_transient_default(self) -> None:
        """Test retry_transient() with defaults"""
        config = resolve_on_error(retry_transient())
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH
        assert config._matchers is not None
        assert len(config._matchers) == 1
        assert isinstance(config._matchers[0], Retry)
        assert config._matchers[0].max_attempts == 3

    def test_retry_transient_custom_attempts(self) -> None:
        """Test retry_transient() with custom max_attempts"""
        config = resolve_on_error(retry_transient(max_attempts=5))
        assert config._matchers is not None
        assert config._matchers[0].max_attempts == 5
        assert config.retry_config.stop.max_attempt_number == 5

    def test_retry_all_default(self) -> None:
        """Test retry_all() with defaults"""
        config = resolve_on_error(retry_all())
        assert config._matchers is not None
        assert len(config._matchers) == 1
        retry = config._matchers[0]
        assert isinstance(retry, Retry)
        assert Exception in retry.exceptions

    def test_retry_all_custom_attempts(self) -> None:
        """Test retry_all() with custom max_attempts"""
        config = resolve_on_error(retry_all(max_attempts=10))
        assert config._matchers is not None
        assert config._matchers[0].max_attempts == 10

    def test_skip_on_error_factory(self) -> None:
        """Test skip_on_error() factory"""
        config = resolve_on_error(skip_on_error())
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS
        assert config._matchers is not None
        assert isinstance(config._matchers[0], Skip)

    def test_fail_fast_factory(self) -> None:
        """Test fail_fast() factory"""
        config = resolve_on_error(fail_fast())
        # Empty list results in default config with no matchers
        assert config._matchers is None
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH

    def test_none_returns_default_config(self) -> None:
        """Test that None returns default error handling"""
        config = resolve_on_error(None)
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH
        assert config._matchers is None

    def test_custom_backoff(self) -> None:
        """Test factory with custom backoff strategy"""
        config = resolve_on_error(retry_transient(backoff="fixed"))
        assert config._matchers is not None
        assert config._matchers[0].backoff == "fixed"


class TestResolveOnError:
    """Tests for resolve_on_error function"""

    def test_resolve_with_matchers(self) -> None:
        """Test resolve_on_error with matcher list"""
        matchers = [
            Retry(ConnectionError, TimeoutError, max_attempts=3),
            Skip(ValueError),
        ]
        config = resolve_on_error(matchers)
        assert config._matchers == matchers
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS  # Has Skip

    def test_resolve_retry_only(self) -> None:
        """Test resolve_on_error with only Retry matchers"""
        matchers = [Retry(ConnectionError, max_attempts=5)]
        config = resolve_on_error(matchers)
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH  # No Skip
        # With per-exception stop, check the max_attempts dict
        assert config.retry_config.stop._max_attempts[ConnectionError] == 5

    def test_resolve_skip_only(self) -> None:
        """Test resolve_on_error with only Skip matchers"""
        matchers = [Skip(ValueError)]
        config = resolve_on_error(matchers)
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS

    def test_different_backoff_strategies_allowed(self) -> None:
        """Test that multiple Retry matchers with different backoffs are allowed"""
        matchers = [
            Retry(ConnectionError, backoff="exponential"),
            Retry(TimeoutError, backoff="fixed"),
        ]
        config = resolve_on_error(matchers)
        assert config._matchers is not None
        assert len(config._matchers) == 2
        # Verify per-exception retry config is created
        assert config.retry_config is not None

    def test_multiple_retry_same_backoff_ok(self) -> None:
        """Test that multiple Retry matchers with same backoff is allowed"""
        matchers = [
            Retry(ConnectionError, backoff="exponential"),
            Retry(TimeoutError, backoff="exponential"),
        ]
        config = resolve_on_error(matchers)
        assert config._matchers is not None
        assert len(config._matchers) == 2

    def test_per_exception_max_attempts(self) -> None:
        """Test that different max_attempts work per exception type"""
        matchers = [
            Retry(ConnectionError, max_attempts=3),
            Retry(TimeoutError, max_attempts=5),
        ]
        config = resolve_on_error(matchers)
        # Should have per-exception stop strategy
        stop = config.retry_config.stop
        # Verify the stop strategy tracks different max_attempts
        assert hasattr(stop, "_max_attempts")
        assert stop._max_attempts[ConnectionError] == 3
        assert stop._max_attempts[TimeoutError] == 5


class TestPerExceptionStrategies:
    """Tests for per-exception wait and stop strategies"""

    def test_per_exception_wait_uses_correct_strategy(self) -> None:
        """Test that _PerExceptionWait uses the correct backoff per exception"""

        from geneva.debug.error_store import _PerExceptionWait

        matchers = [
            Retry(ConnectionError, backoff="exponential"),
            Retry(TimeoutError, backoff="fixed"),
        ]
        wait_strategy = _PerExceptionWait(matchers)

        # Verify different exception types have different wait strategies
        assert wait_strategy._wait_strategies[ConnectionError] is not None
        assert wait_strategy._wait_strategies[TimeoutError] is not None
        # They should be different strategy objects
        assert (
            wait_strategy._wait_strategies[ConnectionError]
            is not wait_strategy._wait_strategies[TimeoutError]
        )

    def test_per_exception_stop_stops_at_correct_attempt(self) -> None:
        """Test that _PerExceptionStop stops at the correct attempt per exception"""
        from unittest.mock import MagicMock

        from geneva.debug.error_store import _PerExceptionStop

        matchers = [
            Retry(ConnectionError, max_attempts=2),
            Retry(TimeoutError, max_attempts=5),
        ]
        stop_strategy = _PerExceptionStop(matchers)

        # Create mock retry states
        def make_retry_state(exc: Exception, attempt: int) -> MagicMock:
            state = MagicMock()
            outcome = MagicMock()
            outcome.exception.return_value = exc
            state.outcome = outcome
            state.attempt_number = attempt
            return state

        # ConnectionError should stop at attempt 2
        assert stop_strategy(make_retry_state(ConnectionError(), 1)) is False
        assert stop_strategy(make_retry_state(ConnectionError(), 2)) is True
        assert stop_strategy(make_retry_state(ConnectionError(), 3)) is True

        # TimeoutError should stop at attempt 5
        assert stop_strategy(make_retry_state(TimeoutError(), 2)) is False
        assert stop_strategy(make_retry_state(TimeoutError(), 4)) is False
        assert stop_strategy(make_retry_state(TimeoutError(), 5)) is True

    def test_per_exception_max_attempt_number_property(self) -> None:
        """Test that max_attempt_number returns the maximum across all exceptions"""
        from geneva.debug.error_store import _PerExceptionStop

        matchers = [
            Retry(ConnectionError, max_attempts=3),
            Retry(TimeoutError, max_attempts=7),
        ]
        stop_strategy = _PerExceptionStop(matchers)

        # max_attempt_number should return the overall max for compatibility
        assert stop_strategy.max_attempt_number == 7


class TestGetExceptionOutcome:
    """Tests for get_exception_outcome function"""

    def test_outcome_retry(self) -> None:
        """Test that Retry matcher returns RETRY outcome"""
        config = resolve_on_error([Retry(ConnectionError)])
        outcome = get_exception_outcome(ConnectionError("test"), config)
        assert outcome == Outcome.RETRY

    def test_outcome_skip(self) -> None:
        """Test that Skip matcher returns SKIP outcome"""
        config = resolve_on_error([Skip(ValueError)])
        outcome = get_exception_outcome(ValueError("test"), config)
        assert outcome == Outcome.SKIP

    def test_outcome_fail(self) -> None:
        """Test that Fail matcher returns FAIL outcome"""
        config = resolve_on_error([Fail(RuntimeError)])
        outcome = get_exception_outcome(RuntimeError("test"), config)
        assert outcome == Outcome.FAIL

    def test_outcome_default_fail(self) -> None:
        """Test that unmatched exceptions return FAIL"""
        config = resolve_on_error([Retry(ConnectionError)])
        outcome = get_exception_outcome(ValueError("test"), config)
        assert outcome == Outcome.FAIL

    def test_outcome_priority(self) -> None:
        """Test that first matching rule wins"""
        config = resolve_on_error(
            [
                Retry(ValueError, match="rate limit"),
                Skip(ValueError),  # Less specific, matches second
            ]
        )
        # Rate limit message should match Retry
        outcome = get_exception_outcome(ValueError("rate limit exceeded"), config)
        assert outcome == Outcome.RETRY

        # Other ValueError should match Skip
        outcome = get_exception_outcome(ValueError("invalid input"), config)
        assert outcome == Outcome.SKIP

    def test_outcome_no_matchers(self) -> None:
        """Test outcome when config has no matchers"""
        config = ErrorHandlingConfig()  # No _matchers
        outcome = get_exception_outcome(ValueError("test"), config)
        assert outcome == Outcome.FAIL


# =============================================================================
# Unit tests for @udf decorator with on_error
# =============================================================================


class TestUdfOnErrorParameter:
    """Tests for the on_error parameter on @udf decorator"""

    def test_udf_with_on_error_factory(self) -> None:
        """Test @udf with on_error factory function"""

        @udf(data_type=pa.int32(), on_error=retry_transient())
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling._matchers is not None

    def test_udf_with_on_error_factory_custom(self) -> None:
        """Test @udf with customized factory function"""

        @udf(data_type=pa.int32(), on_error=retry_transient(max_attempts=7))
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling.retry_config.stop.max_attempt_number == 7

    def test_udf_with_on_error_matchers(self) -> None:
        """Test @udf with on_error matcher list"""

        @udf(
            data_type=pa.int32(),
            on_error=[
                Retry(ConnectionError, max_attempts=5),
                Skip(ValueError),
            ],
        )
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling.fault_isolation == FaultIsolation.SKIP_ROWS
        assert my_udf.error_handling.retry_config.stop.max_attempt_number == 5

    def test_udf_on_error_and_error_handling_conflict(self) -> None:
        """Test that specifying both on_error and error_handling raises error"""
        with pytest.raises(ValueError, match="Cannot specify both"):

            @udf(
                data_type=pa.int32(),
                on_error=retry_transient(),
                error_handling=ErrorHandlingConfig(),
            )
            def my_udf(x: int) -> int:
                return x

    def test_udf_without_on_error(self) -> None:
        """Test that @udf without on_error has no error_handling"""

        @udf(data_type=pa.int32())
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is None


# =============================================================================
# Fixture for integration tests
# =============================================================================


@pytest.fixture
def db(tmp_path) -> Connection:
    """Create a test database with a simple table"""
    tbl_path = tmp_path / "test.lance"

    # Create initial dataset with column 'a'
    data = {"a": pa.array(range(SIZE))}
    tbl = pa.Table.from_pydict(data)
    lance.write_dataset(tbl, tbl_path, max_rows_per_file=10)

    db = geneva.connect(str(tmp_path))
    yield db
    db.close()


# =============================================================================
# Integration tests
# =============================================================================


def test_on_error_retry_transient_integration(db: Connection) -> None:
    """Integration test: on_error=retry_transient() retries network errors"""
    import fcntl
    import tempfile

    # Create unique temp file for atomic counter
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        """Atomically increment counter in file and return new value"""
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(data_type=pa.int32(), on_error=retry_transient())
    def flaky_udf(a: int) -> int:
        count = atomic_increment(counter_file)
        if count < 3:
            raise ConnectionError(f"Temporary failure (attempt {count})")
        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": flaky_udf})

    # Backfill should succeed after retries
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    expected = [x * 2 for x in range(SIZE)]
    assert result_data["b"].to_pylist() == expected

    # Cleanup
    counter_file.unlink(missing_ok=True)


def test_on_error_skip_integration(db: Connection) -> None:
    """Integration test: on_error=skip_on_error() skips failing rows"""

    @udf(data_type=pa.int32(), on_error=skip_on_error())
    def selective_udf(a: int) -> int:
        if a % 3 == 0:  # Skip every 3rd row
            raise ValueError(f"Skipping row {a}")
        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": selective_udf})

    # Backfill should succeed (skipping some rows)
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify results - rows divisible by 3 should be null
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    b_values = result_data["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 3 == 0:
            assert val is None, f"Row {i} should be null"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"


def test_on_error_custom_matchers_integration(db: Connection) -> None:
    """Integration test: on_error with custom matcher list"""
    import fcntl
    import tempfile

    # Create unique temp file for atomic counter
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(
        data_type=pa.int32(),
        on_error=[
            Retry(ConnectionError, max_attempts=3),
            Skip(ValueError),
        ],
    )
    def mixed_udf(a: int) -> int:
        count = atomic_increment(counter_file)

        # First two calls fail with connection error (will retry)
        if count < 3:
            raise ConnectionError(f"Network issue (attempt {count})")

        # Skip every 5th row with ValueError
        if a % 5 == 0:
            raise ValueError(f"Skipping row {a}")

        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": mixed_udf})

    # Backfill should succeed
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    b_values = result_data["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 5 == 0:
            assert val is None, f"Row {i} should be null (skipped)"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"

    # Cleanup
    counter_file.unlink(missing_ok=True)

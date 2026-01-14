"""
pytest-mark-integration plugin

Automatically marks and manages integration tests based on file paths
and provides flexible configuration options.
"""

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item

INTEGRATION_MARK = "integration"

# Global flag to track if any non-integration test has failed
_unit_test_failed = False

# Check if optional dependencies are installed
try:
    import pytest_cov  # type: ignore  # noqa: F401

    HAVE_PYTEST_COV = True
except ImportError:
    HAVE_PYTEST_COV = False

try:
    import pytest_timeout  # type: ignore  # noqa: F401

    HAVE_PYTEST_TIMEOUT = True
except ImportError:
    HAVE_PYTEST_TIMEOUT = False


def pytest_addoption(parser: Parser) -> None:
    """
    Add command line options for controlling integration test execution.

    Args:
        parser: pytest's command line argument parser
    """
    group = parser.getgroup("integration", "Integration test management")

    group.addoption(
        "--with-integration",
        action="store_true",
        dest="run_integration",
        help="Run integration tests (overrides configuration)",
    )

    group.addoption(
        "--without-integration",
        action="store_true",
        dest="skip_integration",
        help="Skip integration tests (overrides configuration)",
    )

    if HAVE_PYTEST_COV:
        group.addoption(
            "--integration-cover",
            action="store_true",
            help="Include integration tests in coverage reports",
        )

    if HAVE_PYTEST_TIMEOUT:
        group.addoption(
            "--integration-timeout",
            type=int,
            default=0,
            help="Set timeout for integration tests (in seconds)",
        )
        group.addoption(
            "--integration-timeout-method",
            type=str,
            default="thread",
            choices=["thread", "signal"],
            help="Timeout method for integration tests",
        )

    # Configuration options (read from pytest.ini or pyproject.toml)
    parser.addini(
        "run_integration_by_default",
        type="bool",
        default=True,
        help="Run integration tests by default (default: True)",
    )

    parser.addini(
        "fail_fast_on_unit_test_failure",
        type="bool",
        default=True,
        help="Skip integration tests if unit tests fail (default: True)",
    )


def pytest_configure(config: Config) -> None:
    """
    Register the integration marker.

    Args:
        config: pytest configuration object
    """
    config.addinivalue_line(
        "markers",
        f"{INTEGRATION_MARK}: mark test as an integration test "
        "(automatically applied to tests in paths containing 'integration')",
    )


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """
    Modify collected test items:
    1. Automatically mark tests in paths containing 'integration'
    2. Sort items: non-integration tests first, integration tests last
    3. Apply additional markers (no_cover, timeout) if plugins are available

    Args:
        config: pytest configuration object
        items: List of collected test items
    """
    # Step 1: Automatically mark integration tests based on file path
    for item in items:
        if _should_mark_as_integration(item):
            item.add_marker(pytest.mark.integration)

    # Step 2: Sort items (non-integration first, integration last)
    items.sort(key=_get_sort_key)

    # Step 3: Apply additional markers for integration tests
    _apply_additional_markers(config, items)


def _should_mark_as_integration(item: Item) -> bool:
    """
    Determine if a test item should be marked as integration.

    A test is considered an integration test if:
    1. It already has the integration marker (manual marking), OR
    2. Its file path relative to rootdir contains 'integration' (case-insensitive)

    Args:
        item: Test item to check

    Returns:
        True if the item should be marked as integration, False otherwise
    """
    # Check if already manually marked
    if item.get_closest_marker(INTEGRATION_MARK):
        return True

    # Get path relative to rootdir to avoid matching parent directory names
    try:
        rootdir = item.session.config.rootpath
        rel_path = item.path.relative_to(rootdir)
        test_path = str(rel_path).lower()
    except (AttributeError, ValueError):
        # Fallback for older pytest versions or if relative path cannot be determined
        test_path = str(item.fspath).lower()

    return "integration" in test_path


def _get_sort_key(item: Item) -> int:
    """
    Get sort key for test item ordering.

    Returns:
        0 for non-integration tests (run first)
        1 for integration tests (run last)
    """
    return 1 if item.get_closest_marker(INTEGRATION_MARK) else 0


def _apply_additional_markers(config: Config, items: list[Item]) -> None:
    """
    Apply additional markers to integration tests based on available plugins.

    Args:
        config: pytest configuration object
        items: List of collected test items
    """
    # Prepare markers
    no_cover_marker = None
    if HAVE_PYTEST_COV and not config.getoption("integration_cover", default=False):
        no_cover_marker = pytest.mark.no_cover

    timeout_marker = None
    timeout_seconds = config.getoption("integration_timeout", default=0)
    if HAVE_PYTEST_TIMEOUT and timeout_seconds > 0:
        timeout_method = config.getoption("integration_timeout_method", default="thread")
        timeout_marker = pytest.mark.timeout(timeout=timeout_seconds, method=timeout_method)

    # Nothing to do if no markers need to be applied
    if not no_cover_marker and not timeout_marker:
        return

    # Apply markers to integration tests
    for item in items:
        if item.get_closest_marker(INTEGRATION_MARK):
            if no_cover_marker:
                item.add_marker(no_cover_marker)
            if timeout_marker:
                item.add_marker(timeout_marker)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: Item) -> None:
    """
    Decide whether to skip integration tests based on:
    1. Command line options (--with-integration / --without-integration)
    2. Configuration (run_integration_by_default)
    3. Fail-fast behavior (fail_fast_on_unit_test_failure)

    Args:
        item: Test item about to be run
    """
    if not item.get_closest_marker(INTEGRATION_MARK):
        # Not an integration test, always run
        return

    # Check fail-fast behavior
    if _should_skip_due_to_fail_fast(item):
        pytest.skip("Skipping integration tests due to unit test failure")

    # Check if we should run integration tests
    if not _should_run_integration_tests(item.config):
        pytest.skip("Integration tests skipped (use --with-integration to run)")


def _should_skip_due_to_fail_fast(item: Item) -> bool:
    """
    Check if integration test should be skipped due to fail-fast behavior.

    Args:
        item: Test item to check

    Returns:
        True if test should be skipped, False otherwise
    """
    global _unit_test_failed

    # Check if fail-fast is enabled
    fail_fast_enabled = item.config.getini("fail_fast_on_unit_test_failure")
    if not fail_fast_enabled:
        return False

    return _unit_test_failed


def _should_run_integration_tests(config: Config) -> bool:
    """
    Determine if integration tests should run based on priority:
    1. Command line options (highest priority)
    2. Configuration (medium priority)
    3. Default behavior (lowest priority)

    Args:
        config: pytest configuration object

    Returns:
        True if integration tests should run, False otherwise
    """
    # Priority 1: Command line options
    if config.getoption("run_integration", default=False):
        return True

    if config.getoption("skip_integration", default=False):
        return False

    # Priority 2 & 3: Configuration (default is True)
    return bool(config.getini("run_integration_by_default"))


def pytest_runtest_makereport(item: Item, call: pytest.CallInfo) -> None:
    """
    Track test failures to implement fail-fast behavior.

    If a non-integration test fails, set a flag to skip subsequent integration tests.

    Args:
        item: Test item that was run
        call: Call information (setup, call, teardown)
    """
    global _unit_test_failed

    # Only care about test call phase (not setup/teardown)
    if call.when != "call":
        return

    # Skip if test passed or was skipped
    if not call.excinfo:
        return

    # Skip if test is marked as xfail (expected failure)
    if item.get_closest_marker("xfail"):
        return

    # If this is a non-integration test that failed, set the flag
    if not item.get_closest_marker(INTEGRATION_MARK):
        _unit_test_failed = True


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """
    Reset global state at the end of the test session.

    Args:
        session: pytest session object
        exitstatus: Exit status code
    """
    global _unit_test_failed
    _unit_test_failed = False

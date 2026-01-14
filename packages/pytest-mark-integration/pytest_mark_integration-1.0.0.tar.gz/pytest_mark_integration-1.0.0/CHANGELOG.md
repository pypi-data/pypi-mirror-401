# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-13

### Changed
- **Python version support**: Dropped support for Python 3.8 and 3.9, added support for Python 3.13 and 3.14. Minimum Python version is now 3.10.
- **Type annotations**: Migrated from `typing.List` to built-in `list` type (available since Python 3.9)
- **Documentation formatting**: Improved table formatting and added spacing for better readability in README.md and PROJECT_SUMMARY.md

### Fixed
- **Improved path detection**: Now uses paths relative to pytest root directory to avoid false positives from parent directory names containing "integration"
- **Test assertions**: Updated test patterns to match actual pytest output
- **Marker detection**: Fixed marker registration test for compatibility with different pytest versions

## [0.1.0] - 2026-01-13

### Added

- **Automatic Integration Test Marking**: Automatically marks tests as integration tests when their file path contains "integration" (case-insensitive)
- **Manual Marking Support**: Allows manual marking with `@pytest.mark.integration` decorator
- **Command-Line Options**:
  - `--with-integration`: Explicitly run integration tests
  - `--without-integration`: Explicitly skip integration tests
  - `--integration-cover`: Include integration tests in coverage reports (requires pytest-cov)
  - `--integration-timeout`: Set timeout for integration tests (requires pytest-timeout)
  - `--integration-timeout-method`: Choose timeout method (thread/signal)
- **Configuration Options**:
  - `run_integration_by_default`: Control whether integration tests run by default (default: `true`)
  - `fail_fast_on_unit_test_failure`: Skip integration tests when unit tests fail (default: `true`)
- **Test Ordering**: Automatically runs unit tests before integration tests for faster feedback
- **Fail-Fast Behavior**: Skips integration tests if any unit test fails (configurable)
- **pytest-cov Integration**: Integration tests excluded from coverage by default
- **pytest-timeout Integration**: Support for setting timeouts specifically for integration tests
- **pytest-xdist Compatibility**: Works with parallel test execution
- **Comprehensive Documentation**: README with examples, troubleshooting, and use cases
- **Architecture Documentation**: Detailed design decisions and implementation details in `docs/architecture.md`

### Technical Details

- Uses pytest hooks: `pytest_addoption`, `pytest_configure`, `pytest_collection_modifyitems`, `pytest_runtest_setup`, `pytest_runtest_makereport`, `pytest_sessionfinish`
- Plugin entry point: `pytest_mark_integration.plugin`
- Compatible with Python 3.8+
- Licensed under Apache-2.0

[Unreleased]: https://github.com/yourusername/pytest-mark-integration/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/pytest-mark-integration/releases/tag/v0.1.0

# Quick Start Guide

Get started with `pytest-mark-integration` in 5 minutes!

## Installation

```bash
pip install pytest-mark-integration
```

Or with uv:

```bash
uv add pytest-mark-integration --dev
```

## Basic Usage

### Step 1: Organize Your Tests

Structure your tests with integration tests in a separate location:

```
your_project/
├── src/
│   └── myapp/
│       └── api.py
└── tests/
    ├── test_utils.py              # Unit tests
    └── integration/
        └── test_api.py             # Integration tests (auto-marked!)
```

### Step 2: Write Tests

**Unit Test** (`tests/test_utils.py`):
```python
def test_helper_function():
    """Fast unit test - runs first"""
    assert my_helper(1, 2) == 3
```

**Integration Test** (`tests/integration/test_api.py`):
```python
import requests

def test_api_endpoint():
    """Slow integration test - runs after unit tests"""
    response = requests.get("http://localhost:8000/api/health")
    assert response.status_code == 200
```

### Step 3: Run Tests

```bash
# Run all tests (default behavior)
pytest

# Skip integration tests (fast local development)
pytest --without-integration

# Run only integration tests
pytest --with-integration -m integration
```

## Configuration

Create `pytest.ini` or add to `pyproject.toml`:

**Option 1: pytest.ini**
```ini
[pytest]
# Skip integration tests by default (good for local dev)
run_integration_by_default = false

# Don't run integration tests if unit tests fail
fail_fast_on_unit_test_failure = true
```

**Option 2: pyproject.toml**
```toml
[tool.pytest.ini_options]
run_integration_by_default = false
fail_fast_on_unit_test_failure = true
```

## Common Workflows

### Local Development (Fast Feedback)

```bash
# In pytest.ini
[pytest]
run_integration_by_default = false
```

```bash
pytest  # Only unit tests run - fast!
```

### CI/CD (Full Testing)

```bash
# In pytest.ini
[pytest]
run_integration_by_default = true
fail_fast_on_unit_test_failure = true
```

```bash
pytest  # All tests run, fail fast on unit test failures
```

### Pre-commit Hook

```bash
pytest --without-integration  # Quick validation
```

### Full Integration Test Suite

```bash
pytest --with-integration -m integration  # Only integration tests
```

## Manual Marking

You can also manually mark tests:

```python
import pytest

@pytest.mark.integration
def test_special_integration():
    """This test is marked even though it's not in 'integration' path"""
    assert True
```

## What Gets Auto-Marked?

Tests are automatically marked as `integration` if their **file path contains "integration"**:

✅ **Auto-marked**:
- `tests/integration/test_api.py`
- `tests/test_database_integration.py`
- `integration_tests/test_system.py`
- `tests/api_integration/test_endpoints.py`

❌ **Not marked**:
- `tests/test_utils.py`
- `tests/unit/test_helpers.py`

## Next Steps

- Read the [full README](../README.md) for detailed documentation
- Check the [architecture docs](architecture.md) for design decisions
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup

## Troubleshooting

### Tests not being marked?

Check that "integration" is in the file path:

```bash
pytest --collect-only  # Shows which tests have the integration marker
```

### Integration tests still running locally?

Set configuration:

```ini
[pytest]
run_integration_by_default = false
```

### Want to include integration tests in coverage?

```bash
pytest --cov --integration-cover
```

## Examples

See the `tests/` directory in this repository for comprehensive examples of all plugin features.

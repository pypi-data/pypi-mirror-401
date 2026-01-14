# Contributing to pytest-mark-integration

Thank you for your interest in contributing to pytest-mark-integration! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pytest-mark-integration.git
   cd pytest-mark-integration
   ```

2. **Install development dependencies**:
   ```bash
   make install-dev
   # or manually:
   uv sync --all-extras
   ```

3. **Verify installation**:
   ```bash
   make test
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run tests with coverage
make test-cov

# Run only integration tests (to test the plugin itself)
make test-integration

# Run only unit tests
make test-unit
```

### Code Quality

```bash
# Format code (black + ruff)
make format

# Lint code
make lint

# Type check
make typecheck

# Run all quality checks
make quality
```

### Before Committing

```bash
# Run all checks (format, lint, typecheck, test)
make pre-commit
```

## Code Style

- **Formatting**: We use [Black](https://black.readthedocs.io/) with a line length of 100
- **Linting**: We use [Ruff](https://docs.astral.sh/ruff/) for linting
- **Type Hints**: We use [mypy](https://mypy.readthedocs.io/) for type checking
- All functions should have type hints
- All public functions should have docstrings

### Example Code Style

```python
"""
Module-level docstring explaining the purpose.
"""

from typing import List, Optional

import pytest
from _pytest.config import Config


def example_function(param: str, optional_param: Optional[int] = None) -> bool:
    """
    Brief description of what this function does.

    Args:
        param: Description of param
        optional_param: Description of optional_param

    Returns:
        Description of return value
    """
    # Implementation
    return True
```

## Testing Guidelines

### Test Structure

- Place tests in the `tests/` directory
- Use descriptive test names: `test_<feature>_<scenario>()`
- Group related tests in the same file
- Use `pytester` fixture for testing pytest plugins

### Example Test

```python
def test_integration_marking_by_path(pytester):
    """Test that files in 'integration' folder are automatically marked."""
    # Arrange
    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_api():
    assert True
"""
        }
    )

    # Act
    result = pytester.runpytest("--without-integration", "-v")

    # Assert
    result.stdout.fnmatch_lines(["*test_api*SKIPPED*"])
```

## Making Changes

### Branch Naming

- Feature branches: `feature/<description>`
- Bug fix branches: `fix/<description>`
- Documentation: `docs/<description>`

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(plugin): add support for custom integration path patterns
fix(sorting): ensure manual markers are sorted correctly
docs(readme): add troubleshooting section
test(config): add tests for configuration priority
```

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the code style guidelines
3. **Add tests** for new features or bug fixes
4. **Update documentation** if needed (README, architecture.md)
5. **Run quality checks**: `make pre-commit`
6. **Update CHANGELOG.md** with your changes under `[Unreleased]`
7. **Submit a pull request** with a clear description

### PR Checklist

- [ ] Tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] No linting errors (`make lint`)
- [ ] Type checks pass (`make typecheck`)
- [ ] Tests added for new features/fixes
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] PR description clearly explains the changes

## Release Process

(For maintainers)

1. **Update version** in `src/pytest_mark_integration/__init__.py`
2. **Update CHANGELOG.md**:
   - Move items from `[Unreleased]` to a new version section
   - Add release date
3. **Commit changes**: `git commit -m "chore: release v0.x.x"`
4. **Create tag**: `git tag v0.x.x`
5. **Push**: `git push && git push --tags`
6. **Build and publish**: `make publish` (or `make publish-test` for testing)

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- Python version
- pytest version
- pytest-mark-integration version
- Minimal reproducible example
- Expected vs actual behavior
- Error messages/traceback

### Feature Requests

When requesting features:

- Clear description of the feature
- Use cases and motivation
- Proposed API (if applicable)
- Willingness to contribute the implementation

## Questions and Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/pytest-mark-integration/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pytest-mark-integration/discussions)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Assume good intentions

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

Thank you for contributing! 🎉

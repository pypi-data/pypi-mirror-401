"""
pytest-mark-integration

A pytest plugin for automatic integration test marking and management.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pytest-mark-integration")
except PackageNotFoundError:
    # Package is not installed (e.g., during development without editable install)
    __version__ = "unknown"

__author__ = "xy.kong"
__email__ = "xy.kong@gmail.com"

# Export commonly used items
from pytest_mark_integration.plugin import INTEGRATION_MARK

__all__ = ["INTEGRATION_MARK", "__version__"]

"""
Example integration test - this file will be auto-marked because 'integration' is in the path.
"""

import pytest


def test_example_integration_auto_marked():
    """
    This test should be automatically marked as integration
    because the filename contains 'integration'.
    """
    assert True


@pytest.mark.integration
def test_example_integration_manual_marked():
    """
    This test is manually marked as integration.
    """
    assert True


def test_another_integration_test():
    """
    Another test that will be auto-marked.
    """
    assert 1 + 1 == 2

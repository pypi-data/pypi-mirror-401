"""
Tests for automatic integration test marking based on file paths.
"""


def test_auto_marking_integration_folder(pytester):
    """Test that tests in 'integration' folder are automatically marked."""
    # Create a test file in an integration folder
    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_api_call():
    assert True
"""
        }
    )

    # Run pytest and collect items
    result = pytester.runpytest("--collect-only", "-q")
    result.assert_outcomes()

    # Run with --without-integration to verify it's marked
    result = pytester.runpytest("--without-integration", "-v")
    result.stdout.fnmatch_lines(["*test_api_call*SKIPPED*"])


def test_auto_marking_integration_filename(pytester):
    """Test that files with 'integration' in name are automatically marked."""
    # Create a test file with 'integration' in its name
    pytester.makepyfile(
        test_db_integration="""
def test_database():
    assert True
"""
    )

    # Run with --without-integration to verify it's marked
    result = pytester.runpytest("--without-integration", "-v")
    result.stdout.fnmatch_lines(["*test_database*SKIPPED*"])


def test_no_auto_marking_unit_test(pytester):
    """Test that unit tests are not automatically marked."""
    # Create a regular unit test
    pytester.makepyfile(
        test_utils="""
def test_helper():
    assert True
"""
    )

    # Run with --without-integration - should not be skipped
    result = pytester.runpytest("--without-integration", "-v")
    result.stdout.fnmatch_lines(["*test_helper*PASSED*"])


def test_manual_marking_overrides(pytester):
    """Test that manual marking works even outside integration paths."""
    # Create a test with manual integration marker
    pytester.makepyfile(
        test_manual="""
import pytest

@pytest.mark.integration
def test_manually_marked():
    assert True
"""
    )

    # Run with --without-integration to verify it's marked
    result = pytester.runpytest("--without-integration", "-v")
    result.stdout.fnmatch_lines(["*test_manually_marked*SKIPPED*"])

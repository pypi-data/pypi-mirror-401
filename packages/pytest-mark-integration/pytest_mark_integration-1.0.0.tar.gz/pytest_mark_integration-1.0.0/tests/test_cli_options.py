"""
Tests for command-line options (--with-integration and --without-integration).
"""


def test_with_integration_flag(pytester):
    """Test that --with-integration runs integration tests."""
    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        }
    )

    result = pytester.runpytest("--with-integration", "-v")
    result.stdout.fnmatch_lines(["*test_integration_api*PASSED*"])


def test_without_integration_flag(pytester):
    """Test that --without-integration skips integration tests."""
    pytester.makepyfile(
        test_unit="""
def test_unit():
    assert True
""",
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        },
    )

    result = pytester.runpytest("--without-integration", "-v")
    result.stdout.fnmatch_lines(
        [
            "*test_unit*PASSED*",
            "*test_integration_api*SKIPPED*",
        ]
    )


def test_without_integration_shows_skip_message(pytester):
    """Test that skipped integration tests show appropriate message."""
    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        }
    )

    result = pytester.runpytest("--without-integration", "-v")
    result.stdout.fnmatch_lines(["*SKIPPED*Integration*"])


def test_with_and_without_conflict(pytester):
    """Test behavior when both --with and --without are specified."""
    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        }
    )

    # --with-integration should take precedence (it's checked first in code)
    result = pytester.runpytest("--with-integration", "--without-integration", "-v")
    result.stdout.fnmatch_lines(["*test_integration_api*PASSED*"])

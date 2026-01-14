"""
Tests for configuration options (run_integration_by_default, fail_fast_on_unit_test_failure).
"""


def test_run_integration_by_default_true(pytester):
    """Test that integration tests run by default when configured."""
    pytester.makeini(
        """
[pytest]
run_integration_by_default = true
"""
    )

    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        }
    )

    # Run without any flags - should run integration tests
    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(["*test_integration_api*PASSED*"])


def test_run_integration_by_default_false(pytester):
    """Test that integration tests are skipped by default when configured."""
    pytester.makeini(
        """
[pytest]
run_integration_by_default = false
"""
    )

    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        }
    )

    # Run without any flags - should skip integration tests
    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(["*test_integration_api*SKIPPED*"])


def test_cli_overrides_config(pytester):
    """Test that CLI options override configuration."""
    pytester.makeini(
        """
[pytest]
run_integration_by_default = false
"""
    )

    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        }
    )

    # --with-integration should override config
    result = pytester.runpytest("--with-integration", "-v")
    result.stdout.fnmatch_lines(["*test_integration_api*PASSED*"])


def test_fail_fast_on_unit_test_failure(pytester):
    """Test that integration tests are skipped when unit tests fail."""
    pytester.makeini(
        """
[pytest]
fail_fast_on_unit_test_failure = true
"""
    )

    pytester.makepyfile(
        test_unit="""
def test_unit_fails():
    assert False, "Unit test failure"
""",
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        },
    )

    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(
        [
            "*test_unit_fails*FAILED*",
            "*test_integration_api*SKIPPED*Skipping inte*",
        ]
    )


def test_fail_fast_disabled(pytester):
    """Test that integration tests run even when unit tests fail if disabled."""
    pytester.makeini(
        """
[pytest]
fail_fast_on_unit_test_failure = false
"""
    )

    pytester.makepyfile(
        test_unit="""
def test_unit_fails():
    assert False, "Unit test failure"
""",
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        },
    )

    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(
        [
            "*test_unit_fails*FAILED*",
            "*test_integration_api*PASSED*",
        ]
    )


def test_fail_fast_only_affects_integration_tests(pytester):
    """Test that fail-fast only affects integration tests, not other unit tests."""
    pytester.makeini(
        """
[pytest]
fail_fast_on_unit_test_failure = true
"""
    )

    pytester.makepyfile(
        test_unit_first="""
def test_unit_fails():
    assert False, "Unit test failure"
""",
        test_unit_second="""
def test_another_unit():
    assert True
""",
        **{
            "integration/test_api.py": """
def test_integration_api():
    assert True
"""
        },
    )

    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(
        [
            "*test_unit_fails*FAILED*",
            "*test_another_unit*PASSED*",  # Other unit tests still run
            "*test_integration_api*SKIPPED*",  # Integration tests are skipped
        ]
    )

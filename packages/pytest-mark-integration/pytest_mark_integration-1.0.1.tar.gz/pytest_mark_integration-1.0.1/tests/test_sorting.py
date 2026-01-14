"""
Tests for test ordering (unit tests run before integration tests).
"""


def test_unit_tests_run_before_integration(pytester):
    """Test that unit tests are executed before integration tests."""
    pytester.makepyfile(
        **{
            "integration/test_integration_first.py": """
def test_integration():
    print("INTEGRATION TEST")
    assert True
""",
            "test_unit.py": """
def test_unit():
    print("UNIT TEST")
    assert True
""",
        }
    )

    result = pytester.runpytest("-v", "-s")

    # Check that output shows unit test before integration test
    output = result.stdout.str()
    unit_pos = output.find("UNIT TEST")
    integration_pos = output.find("INTEGRATION TEST")

    assert unit_pos < integration_pos, "Unit tests should run before integration tests"


def test_multiple_integration_tests_order(pytester):
    """Test ordering with multiple unit and integration tests."""
    pytester.makepyfile(
        **{
            "integration/test_api.py": """
def test_api():
    assert True
""",
            "integration/test_database.py": """
def test_database():
    assert True
""",
            "test_unit_a.py": """
def test_unit_a():
    assert True
""",
            "test_unit_b.py": """
def test_unit_b():
    assert True
""",
        }
    )

    result = pytester.runpytest("--collect-only", "-q")
    output = result.stdout.str()

    # Find positions of test types
    lines = output.split("\n")
    test_lines = [line for line in lines if "::test_" in line]

    # Count unit tests that appear before first integration test
    unit_tests = [line for line in test_lines if "integration" not in line.lower()]
    integration_tests = [line for line in test_lines if "integration" in line.lower()]

    # All unit tests should appear before integration tests
    if integration_tests:
        first_integration_idx = test_lines.index(integration_tests[0])
        unit_before_integration = [
            line for line in unit_tests if test_lines.index(line) < first_integration_idx
        ]
        assert len(unit_before_integration) == len(
            unit_tests
        ), "All unit tests should come before integration tests"


def test_manually_marked_integration_sorted_correctly(pytester):
    """Test that manually marked integration tests are also sorted correctly."""
    pytester.makepyfile(
        test_unit="""
def test_unit():
    print("UNIT")
    assert True
""",
        test_manual_integration="""
import pytest

@pytest.mark.integration
def test_manually_marked():
    print("MANUAL INTEGRATION")
    assert True
""",
    )

    result = pytester.runpytest("-v", "-s")

    output = result.stdout.str()
    unit_pos = output.find("UNIT")
    manual_integration_pos = output.find("MANUAL INTEGRATION")

    assert (
        unit_pos < manual_integration_pos
    ), "Manually marked integration tests should also run after unit tests"

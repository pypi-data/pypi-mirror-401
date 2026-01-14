"""
Basic tests for pytest-mark-integration plugin functionality.
"""


def test_plugin_loaded(pytestconfig):
    """Test that the plugin is loaded."""
    assert pytestconfig.pluginmanager.has_plugin("pytest_mark_integration")


def test_integration_marker_registered(pytestconfig):
    """Test that the integration marker is registered."""
    markers = pytestconfig.getini("markers")
    marker_names = " ".join(markers)
    assert "integration" in marker_names


def test_command_line_options_registered(pytestconfig):
    """Test that command line options are registered."""
    # Check if options exist (they might not have values set)
    assert hasattr(pytestconfig.option, "run_integration")
    assert hasattr(pytestconfig.option, "skip_integration")

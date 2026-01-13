"""Tests for configure_excel_no_alerts function."""

from xlwings_macos_utils.core import configure_excel_no_alerts


def test_configure_excel_success(mock_subprocess_success, capsys):
    """Test successful Excel configuration."""
    configure_excel_no_alerts()
    
    captured = capsys.readouterr()
    assert "[CONFIG] Excel configured to suppress alerts" in captured.out


def test_configure_excel_called_process_error(mock_subprocess_error, capsys):
    """Test handling of CalledProcessError."""
    configure_excel_no_alerts()
    
    captured = capsys.readouterr()
    assert "[WARNING] Could not configure Excel alerts" in captured.out


def test_configure_excel_timeout(mock_subprocess_timeout, capsys):
    """Test handling of TimeoutExpired."""
    configure_excel_no_alerts()
    
    captured = capsys.readouterr()
    assert "[WARNING] Timeout while configuring Excel" in captured.out

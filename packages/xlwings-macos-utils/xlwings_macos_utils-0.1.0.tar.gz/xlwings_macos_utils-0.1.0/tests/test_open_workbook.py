"""Tests for open_workbook_with_workaround function."""

from unittest.mock import Mock, MagicMock

from xlwings_macos_utils.core import open_workbook_with_workaround


def test_open_workbook_already_open(mock_excel_app, mock_workbook, capsys):
    """Test that already open workbooks are detected and returned."""
    mock_excel_app.books = [mock_workbook]
    
    result = open_workbook_with_workaround(mock_excel_app, "/path/to/test_file.xlsx")
    
    assert result == mock_workbook
    captured = capsys.readouterr()
    assert "already open" in captured.out


def test_open_workbook_success(mock_excel_app, mock_workbook, monkeypatch, capsys):
    """Test successful workbook opening via AppleScript."""
    mock_run = Mock()
    mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
    monkeypatch.setattr("subprocess.run", mock_run)
    monkeypatch.setattr("time.sleep", lambda x: None)
    
    mock_excel_app.books = MagicMock()
    mock_excel_app.books.__iter__.return_value = []
    mock_excel_app.books.__getitem__.return_value = mock_workbook
    
    result = open_workbook_with_workaround(mock_excel_app, "/path/to/test_file.xlsx")
    
    assert result == mock_workbook
    captured = capsys.readouterr()
    assert "Successfully connected" in captured.out


def test_open_workbook_subprocess_error(mock_excel_app, mock_subprocess_error, capsys):
    """Test handling of subprocess CalledProcessError."""
    result = open_workbook_with_workaround(mock_excel_app, "/path/to/test.xlsx")
    
    assert result is None
    captured = capsys.readouterr()
    assert "[ERROR] Failed to open" in captured.out


def test_open_workbook_connection_failure(mock_excel_app, monkeypatch, capsys):
    """Test failure after all connection attempts."""
    mock_run = Mock()
    mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
    monkeypatch.setattr("subprocess.run", mock_run)
    monkeypatch.setattr("time.sleep", lambda x: None)
    
    mock_excel_app.books = MagicMock()
    mock_excel_app.books.__iter__.return_value = []
    mock_excel_app.books.__getitem__.side_effect = Exception("File not found")
    
    result = open_workbook_with_workaround(mock_excel_app, "/path/to/test.xlsx")
    
    assert result is None
    captured = capsys.readouterr()
    assert "[ERROR] Could not connect to workbook" in captured.out

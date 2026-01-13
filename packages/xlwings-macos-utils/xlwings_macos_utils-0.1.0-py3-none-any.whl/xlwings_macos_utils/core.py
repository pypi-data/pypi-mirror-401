"""
Core functionality for xlwings macOS utilities.

This module provides functions to work around macOS-specific issues when
automating Excel with xlwings, including:
- File permission dialogs that block script execution
- External links update prompts
"""

import os
import subprocess
import time
from typing import Optional

import xlwings as xw


def configure_excel_no_alerts() -> None:
    """
    Configure Excel via AppleScript to disable alerts and external links update prompts.
    
    This function uses AppleScript to set Excel preferences that prevent it from
    showing dialog boxes that would block automation scripts. It specifically:
    - Disables the external links update prompt
    - Disables general alert dialogs
    
    Important:
        Call this function ONCE at the beginning of your script, before opening
        any Excel files.
    
    Raises:
        No exceptions are raised. Errors are logged but execution continues.
    
    Example:
        >>> from xlwings_macos_utils import configure_excel_no_alerts
        >>> configure_excel_no_alerts()
        [CONFIG] Excel configured to suppress alerts and external link prompts.
    """
    script = '''
    tell application "Microsoft Excel"
        -- Disable external links update prompt
        set ask to update links to false
        -- Disable general alerts
        set display alerts to false
    end tell
    '''
    try:
        subprocess.run(
            ['osascript', '-e', script],
            check=True,
            timeout=10,
            capture_output=True
        )
        print("[CONFIG] Excel configured to suppress alerts and external link prompts.")
    except subprocess.CalledProcessError as e:
        print(f"[WARNING] Could not configure Excel alerts: {e}")
        print("         Excel may show dialog boxes that block automation.")
    except subprocess.TimeoutExpired:
        print("[WARNING] Timeout while configuring Excel, continuing anyway...")


def open_workbook_with_workaround(
    app_excel: xw.App,
    file_path: str
) -> Optional[xw.Book]:
    """
    Open an Excel workbook on macOS using a workaround for the permission dialog.
    
    This function works around the macOS file permission dialog ("Grant Access")
    that blocks xlwings when opening files. It uses AppleScript to open the file
    in a non-blocking manner, then connects to it via xlwings.
    
    Args:
        app_excel: The xlwings Excel application instance (from xw.App()).
        file_path: The absolute path to the Excel file (.xlsx, .xlsm, etc.) to open.
    
    Returns:
        The xlwings workbook object if successful, None if the operation fails.
    
    Note:
        Call configure_excel_no_alerts() BEFORE using this function to prevent
        external links update prompts.
    
    Example:
        >>> import xlwings as xw
        >>> from xlwings_macos_utils import configure_excel_no_alerts, open_workbook_with_workaround
        >>> 
        >>> configure_excel_no_alerts()
        >>> app = xw.App(visible=False, add_book=False)
        >>> wb = open_workbook_with_workaround(app, '/path/to/file.xlsx')
        >>> if wb:
        ...     print(f"Opened: {wb.name}")
        ...     wb.close()
        >>> app.quit()
    
    Raises:
        No exceptions are raised. Errors are logged and None is returned on failure.
    """
    filename = os.path.basename(file_path)
    
    # Check if the file is already open to avoid reopening it
    try:
        for book in app_excel.books:
            if book.name == filename:
                print(f"  [INFO] File '{filename}' is already open. Connecting to it.")
                return book
    except Exception:
        # If listing books fails, continue trying to open
        pass

    # AppleScript to open the file
    # Global settings (ask to update links, display alerts) should already be
    # configured by configure_excel_no_alerts(), so Excel won't show prompts
    applescript = f'''
tell application "Microsoft Excel"
    set display alerts to false
    set ask to update links to false
    open POSIX file "{file_path}"
    set visible to false
end tell
'''

    try:
        # Execute the command to open the file
        result = subprocess.run(
            ['osascript', '-e', applescript],
            check=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        if result.stderr:
            print(f"  [DEBUG] stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Failed to open '{filename}' via osascript.")
        print(f"          Error: {e.stderr if e.stderr else e}")
        print(f"          Make sure the file exists and Excel is installed.")
        return None
    except subprocess.TimeoutExpired:
        print(f"  [WARNING] Opening '{filename}' took too long, but may have succeeded.")
        # Continue anyway, as the command may have been sent successfully

    # Give Excel time to process the file opening before trying to connect
    time.sleep(0.1)

    # Connect to the now-open workbook using xlwings
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            workbook = app_excel.books[filename]
            print(f"  [INFO] Successfully connected to '{filename}' via workaround.")
            return workbook
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(1)
            else:
                print(f"  [ERROR] Could not connect to workbook '{filename}' after opening.")
                print(f"          Error: {e}")
                print(f"          The file may not have opened or may have a different name.")
                return None
    
    return None

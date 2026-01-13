"""
xlwings-macos-utils: Utilities to solve macOS-specific issues with xlwings.

This library provides workarounds for common problems when using xlwings on macOS,
particularly the file permission dialog that blocks script execution and the
external links update prompt.
"""

from xlwings_macos_utils.core import (
    configure_excel_no_alerts,
    open_workbook_with_workaround,
)

__version__ = "0.1.0"
__all__ = ["configure_excel_no_alerts", "open_workbook_with_workaround"]

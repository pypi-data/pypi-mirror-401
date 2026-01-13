# xlwings-macos-utils

[![PyPI version](https://badge.fury.io/py/xlwings-macos-utils.svg)](https://badge.fury.io/py/xlwings-macos-utils)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Workarounds for macOS-specific issues when automating Excel with [xlwings](https://www.xlwings.org/).

## The Problem

On macOS, xlwings users face two blocking issues:

1. **File Permission Dialog (Error -1743)** - macOS shows a "Grant Access" dialog that freezes script execution
2. **External Links Update Prompt** - Excel asks to update external links on every file open

These are well-documented issues: [#1966](https://github.com/xlwings/xlwings/issues/1966), [#2559](https://github.com/xlwings/xlwings/issues/2559), [#1262](https://github.com/xlwings/xlwings/issues/1262)

## Installation

```bash
pip install xlwings-macos-utils
```

**Requirements:** macOS 10.14+, Microsoft Excel, Python 3.8+, xlwings 0.27.0+

## Quick Start

```python
import xlwings as xw
from xlwings_macos_utils import configure_excel_no_alerts, open_workbook_with_workaround

# Step 1: Configure Excel (call once at start)
configure_excel_no_alerts()

# Step 2: Create Excel app
app = xw.App(visible=False, add_book=False)

try:
    # Step 3: Open workbook using the workaround
    wb = open_workbook_with_workaround(app, '/path/to/file.xlsx')
    
    if wb:
        # Your automation code here
        sheet = wb.sheets[0]
        data = sheet.range('A1:C10').value
        print(f"Read data from {wb.name}")
        wb.close()
finally:
    app.quit()
```

## API

### `configure_excel_no_alerts()`

Configures Excel via AppleScript to suppress alerts and external link prompts.

**Important:** Call once at the beginning of your script, before opening any files.

### `open_workbook_with_workaround(app_excel, file_path)`

Opens an Excel workbook using AppleScript to bypass the permission dialog.

**Parameters:**
- `app_excel` (xw.App): The xlwings Excel application instance
- `file_path` (str): Absolute path to the Excel file

**Returns:** `xw.Book` if successful, `None` on failure

## How It Works

Uses AppleScript to:
1. Configure Excel settings (`set display alerts to false`, `set ask to update links to false`)
2. Open files via `open POSIX file` (non-blocking)
3. Connect via xlwings with automatic retry

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Could not configure Excel alerts" | Ensure Excel is installed |
| "Failed to open via osascript" | Verify file path is correct and absolute |
| "Could not connect to workbook" | Check if Excel is responsive, try increasing retry delay |
| Still getting permission dialogs | Ensure `configure_excel_no_alerts()` is called first |

## Contributing

```bash
git clone https://github.com/andreggalvao/xlwings-macos-utils.git
cd xlwings-macos-utils
pip install -e ".[dev]"
pytest
```

## License

MIT - see [LICENSE](LICENSE)

## Related Issues

- [#1966](https://github.com/xlwings/xlwings/issues/1966) - OSERROR: -1743 MESSAGE: The user has declined permission
- [#2559](https://github.com/xlwings/xlwings/issues/2559) - Unusual file open errors
- [#1262](https://github.com/xlwings/xlwings/issues/1262) - OS error: -1743 (21 comments)

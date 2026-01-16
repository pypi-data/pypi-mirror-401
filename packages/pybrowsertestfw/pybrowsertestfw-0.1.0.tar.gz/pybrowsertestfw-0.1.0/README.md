# pybrowsertestfw Module and Sample Project

## 1. pybrowsertestfw Module Overview

This project provides a lightweight test automation core module based on pytest, targeting a unified usage pattern and reporting output for Web (Selenium) and mobile (Appium). It is ready to use with a “convention over configuration” style. Once installed from PyPI as `pybrowsertestfw`, it can be reused in any project.

### Positioning
- Unified: Web and mobile operations share the same abstraction, and screenshot/report paths are consistent.
- Simple: Zero-parameter default behaviors (such as `WebActions.screenshot()`), with a minimal usable API set.
- Visible: Built-in HTML, PDF, and JSON reports, automatically attaching screenshots and runtime logs.

### Features
- Reports and attachments
  - Automatically generates `reports/<ts>/report_<ts>.html`, `report_<ts>.pdf`, and `report_<ts>.json`.
  - Screenshots are uniformly named `screenshot/ss_{YYYYMMDD_HHMMSS}.png` and injected into the report.
- Logging
  - Root log is written to `reports/<ts>/framework_<ts>.log`.
  - Provides `get_logger(name)` to obtain a named logger consistently.
- Minimal APIs
  - Direct attach: `capture_and_attach(config, rep, driver, label)`.
  - Queue-based: `capture_and_queue_simple(driver)` plus a unified attach step in plugin hooks.

### Installation and Integration
```bash
pip install pybrowsertestfw
```
Or add the dependency to your existing `pyproject.toml`:
```toml
[project]
dependencies = [
  "pybrowsertestfw>=0.1.0",
]
```
After installation, pytest will automatically load the plugin `framework.pytest_plugin` via entry points, no extra parameters required.

> Python version requirement: supports Python 3.9.x - 3.13.x (`requires-python = ">=3.9, <3.14"`).

### Module Directory (Simplified)
```
├── framework/
│   ├── config.py              # CLI/session configuration parsing
│   ├── driver_factory.py      # WebDriver/Appium driver creation
│   ├── logger.py              # Logging configuration and entry
│   ├── reporting.py           # Reporting and screenshots
│   ├── order.py               # Test ordering logic (no pytest-order required)
│   ├── pdf_report.py          # Optional PDF report generation
│   └── pytest_plugin.py       # Framework hooks and context
├── operations/
│   └── web.py                 # WebActions wrapper
└── video/
    └── recorder.py            # Screen recording implementation (Web/Appium)
```

This repository only contains reusable framework core code (released as the `pybrowerstestfw` package).

## 2. Create a Sample Project

The following uses a minimal sample project to demonstrate how to quickly set up and run locally.

### Directory Layout
```
├── drivers/
│   └── chromedriver.exe
├── properties.yml
├── pytest.ini
├── requirements.txt
├── test_order.yml
├── tests/
│   └── test_sample.py
├── datas/         # Optional
|   └── data.csv
└── reports/       # Generated at runtime
|   └── <ts>/
|       ├── report_<ts>.html
|       ├── report_<ts>.pdf
|       ├── report_<ts>.json
|       ├── framework_<ts>.log
|       └── screenshot/
|           └── ss_*.png
```

### Browser and Mobile Drivers
- Path consistency: All desktop browser drivers should be placed in the `drivers/` directory under the project root (lowercase).
- Version matching: Each browser driver’s major version must match the corresponding browser’s major version on the machine, otherwise session creation may fail.
- Desktop examples:
  - In `properties.yml`, point `executable_path` to the corresponding file <mark>(Safari excluded)</mark>.
  - Chrome: example path `.\\drivers\\chromedriver.exe`.
  - Edge: example path `.\\drivers\\msedgedriver.exe`.
  - Firefox: example path `.\\drivers\\geckodriver.exe`.
  - Safari (macOS): uses the system `safaridriver`. Run `safaridriver --enable` on macOS to pre-authorize; no local `executable_path` is needed.
- Mobile examples:
  - Android: set `'appium:chromedriverExecutable'` in capabilities to a valid ChromeDriver absolute path, for example `'C:\\Drivers\\chromedriver.exe'`, to drive mobile Chrome/WebView.
  - iOS: connect real devices or simulators through Appium, which relies on the device’s `safaridriver` capabilities. No additional browser driver files are required in the project.
- Remote mode: When connecting to Selenium Grid, local `executable_path` is usually unnecessary; driver versions are managed on the remote side.

### Quick Start

**1. Create a project directory and enter it, for example:**
```bash
mkdir my_sample_project
cd my_sample_project
```

**2. Create and activate a virtual environment (recommended):**
- Windows (PowerShell):
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- Windows (cmd):
  ```bat
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```
- macOS / Linux (shell):
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  ```

**3. Create and fill `requirements.txt`:**
```text
pybrowerstestfw>=0.1.0
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Create `pytest.ini`:**
```ini
[pytest]
markers =
    smoke: 'smoke test'
addopts = --strict
```

**6. Create `properties.yml`:**
```yaml
# This is an example of Chrome configuration.
chrome:
  browserName: 'chrome'
  executable_path: '.\\drivers\\chromedriver.exe'
  'goog:chromeOptions':
    args:
      - '--start-maximized'
    experimentalOptions:
      excludeSwitches:
        - 'enable-automation'
```

**7. Create `test_order.yml` (optional, to control execution order):**
```yaml
- "tests/test_sample.py::test_demo_aut"
```

**8. Create a sample test `tests/test_sample.py`**
  - Example 1:
    - Test case without CSV:
      ```python
      import pytest
      from selenium.webdriver.common.by import By


      @pytest.mark.smoke
      def test_demo_aut(driver, acts: WebActions):
          driver.get("https://katalon-test.s3.amazonaws.com/aut/html/form.html")
          driver.find_element(By.ID, "first-name").clear()
          driver.find_element(By.ID, "first-name").send_keys("Alex")
          driver.find_element(By.ID, "last-name").clear()
          driver.find_element(By.ID, "last-name").send_keys("Smith")
          acts.screenshot()
      ```

- Example 2:
  - Test case using CSV:
    ```python
    import pytest
    from selenium.webdriver.common.by import By

    from operations.web import WebActions


    @pytest.mark.smoke
    def test_demo_aut(driver, acts: WebActions):
        rows = acts.load_vars_from_csv("data.csv")
        for row in rows:
            first = row.get("first", "")
            last = row.get("last", "")

            driver.get("https://katalon-test.s3.amazonaws.com/aut/html/form.html")
            driver.find_element(By.ID, "first-name").clear()
            driver.find_element(By.ID, "first-name").send_keys(first)
            driver.find_element(By.ID, "last-name").clear()
            driver.find_element(By.ID, "last-name").send_keys(last)

            acts.screenshot()
    ```

  - Create test data file `datas/data.csv`:
    ```text
    first,last
    Alex,Smith
    Steve,Rogers
    ```

**9. Run the sample test**
```bash
pytest --profile="chrome" -q tests/test_sample.py
```

**10. Open the reports**
- HTML: `reports/<ts>/report_<ts>.html`
- JSON: `reports/<ts>/report_<ts>.json`
- PDF: `reports/<ts>/report_<ts>.pdf`
- Log: `reports/<ts>/framework_<ts>.log`
- Screenshots: `reports/<ts>/screenshot/ss_*.png`

### Basic Usage
- Get a named logger
```python
from framework.logger import get_logger
logger = get_logger("operations.web")
```
- Example usage of `screenshot`
```python
from operations.web import WebActions

web = WebActions(driver)
web.screenshot()
```
- Example usage of `load_vars_from_csv`
```python
from operations.web import WebActions

def test_sample_two(driver, acts: WebActions):
  rows = acts.load_vars_from_csv("data.csv")
  for row in rows:
      first = row.get("first", "")
      last = row.get("last", "")

      driver.get("https://katalon-test.s3.amazonaws.com/aut/html/form.html")
      driver.find_element(By.ID, "first-name").clear()
      driver.find_element(By.ID, "first-name").send_keys(first)
      driver.find_element(By.ID, "last-name").clear()
      driver.find_element(By.ID, "last-name").send_keys(last)
```

### Configuration
- `requirements.txt`: Declare project dependencies, at least `pybrowerstestfw`, `pytest`, and `selenium`.
- `pytest.ini`: Pytest global configuration, defines markers and strict mode.
- `properties.yml`: Stores browser/device capabilities (caps) that the framework reads to create corresponding drivers.
- `test_order.yml`: Optional, used to specify test execution order.
- At session start, the plugin automatically:
  - Initializes report directories and filenames (`init_reporting`).
  - Configures the root logger (`setup_logging`).

### Reporting and Screenshot Flow
- During test execution: `WebActions.screenshot()` → `capture_and_queue_simple(driver)` saves PNG files and enqueues them.
- Reporting phase: The plugin triggers `drain_pending_extras`, attaching all queued images to the HTML report via `rep.extras`.
- JSON report: Automatically injects a `screenshots` field with relative paths.

### Test Ordering (Without pytest-order)
- Supports controlling execution order via the `test_order.yml` manifest, without modifying test files, and is compatible with Katalon scripts exported in bulk or individually.
- Usage:
  - Create `test_order.yml` in the project root. Each item is a NodeID pattern (YAML list), matched in declared order:
    - `tests/test_login.py::test_login`
    - `tests/test_saucedemo_v2.py::test_*`
    - `tests/generated/**/test_*.py::test_*`
  - Verify collection order: `pytest --collect-only -p no:order`
- Notes:
  - The framework registers `pytest_collection_modifyitems` in the plugin and delegates to `framework/order.py`. If `pytest-order` is also installed, it may reorder items again after collection; it is recommended to disable it via `-p no:order` or remove it from dependencies.
  - Items not matched in `test_order.yml` maintain default ordering and run after matched items. Parallel execution (`pytest-xdist`) may break ordering; disable parallelism or use single-test orchestration when strict ordering is required.

### Extension Points
- Custom CLI options
  - `--profile`: Specify the capabilities key (caps) in `properties.yml`. Example: `--profile web_chrome`.
  - `--remote-address`: Remote WebDriver/Appium address. Example (Selenium Grid): `http://localhost:4444/wd/hub`; example (Appium): `http://127.0.0.1:4723/wd/hub`.
  - `--video`: Whether to record video (`y|n`, default `n`). Output file: `reports/<ts>/video_<ts>.mp4`.
  - Notes: For Web (Selenium) it uses a built-in screen recorder (bundled in `video/pyscreenrec.py`) to capture the entire screen (non-headless is recommended). For mobile (Appium) it uses the driver’s built-in recording.
  - Examples:
    ```bash
    # Local browser (Chrome, local driver)
    pytest --profile="chrome" -m "smoke"
    
    # Remote Selenium Grid (Chrome)
    pytest --profile="chrome" --remote-address="http://localhost:4444/wd/hub" -m "smoke"
    
    # Appium (mobile Web): requires remote mode + browserName
    pytest --profile="android_chrome" --remote-address="http://127.0.0.1:4723/wd/hub" -m "smoke" --video="y"
    
    # Local browser (Edge)
    pytest --profile="edge_local" -m "smoke"
    
    # Local browser (Firefox)
    pytest --profile="firefox_local" -m "smoke"
    
    # Safari (macOS only)
    pytest --profile="safari_mac" -m "smoke"
    ```

- Appium usage example (mobile Web)
  - `properties.yml` example:
    ```yaml
    android_chrome:
      platformName: 'Android'
      browserName: 'chrome'
      'appium:automationName': 'UiAutomator2'
      'appium:deviceName': 'emulator-5554'
      'appium:noReset': true
      'appium:chromedriverExecutable': 'C:\\Drivers\\chromedriver.exe'
      'goog:chromeOptions':
        experimentalOptions:
          w3c: false

    ios_safari:
      platformName: 'iOS'
      browserName: 'safari'
      'appium:automationName': 'XCUITest'
      'appium:deviceName': 'iPhone 15'
      'appium:udid': '000XXX20-001C35XXXE42XXXX'
      'appium:noReset': true
      'appium:nativeWebTap': true
      'appium:safariAllowPopups': false
      'appium:safariIgnoreFraudWarning': true
    ```
  - Run example:
    ```bash
    # Android Chrome (ensure Appium Server is running)
    pytest --profile="android_chrome" --remote-address="http://127.0.0.1:4723/wd/hub" -m "smoke"
    ```
  - Note: The current version requires `browserName` in `capabilities` (for mobile Web/WebView).

### Locator Strategy Compatibility (Mobile Web / Appium)
- In mobile Web sessions through Appium→WebDriver, the server enforces locator strategies more strictly. Directly using `using: "id"|"name"|"class name"` may be considered invalid and return `invalid locator` (400).
- If test cases call `driver.find_element("id", ...)` directly, mobile Web scenarios may still fail. Using CSS or XPath locators is recommended.

### FAQ
- Screenshots not visible? Ensure you are using a `pytest-html` version that supports `rep.extras` (4.1.x or above).
- Paths too long? The framework removes `nodeid` in filenames and uses timestamps to keep them short and consistent.

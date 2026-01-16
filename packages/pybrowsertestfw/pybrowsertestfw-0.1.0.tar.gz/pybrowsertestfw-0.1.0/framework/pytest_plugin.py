from typing import Any, Dict
import pytest
import time

from .reporting import init_reporting, capture_and_attach, inject_screenshots, drain_pending_extras, set_current_nodeid
from .logger import setup_logging

from . import driver_factory, config as cf
from video import start_video_if_enabled, stop_video_if_enabled

from operations.web import WebActions
from . import order as ord


# --- CLI Options ---
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--profile",
        action="store",
        default=None,
        help="Key in properties.yml to select capabilities",
    )
    parser.addoption(
        "--remote-address",
        action="store",
        default=None,
        help="Remote WebDriver/Appium server URL (e.g., http://127.0.0.1:8094/wd/hub)",
    )
    parser.addoption(
        "--video",
        action="store",
        default="n",
        help="Enable video recording after driver created (y/n). Default: n",
    )


# --- Reporting setup ---
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    # Initialize report & screenshot directories and default html/json outputs
    init_reporting(config)
    # Initialize logging to reports/<ts>/framework_<ts>.log
    setup_logging(config)


# --- Screenshot attach via test reports ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    rep = outcome.get_result()

    # Get driver (prefer function-level, otherwise use session-level)
    driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if driver is None:
        driver = getattr(item.config, "_session_driver", None)
    if driver is None:
        return

    # Attach any queued screenshots requested by WebActions or other helpers
    drain_pending_extras(item.config, rep)

    # Success case: capture screenshot after call by default
    if rep.when == "call" and not rep.failed:
        capture_and_attach(item.config, rep, driver, label="after call")

    # Failure case: capture screenshot at whatever phase failed
    if rep.failed:
        capture_and_attach(item.config, rep, driver, label=f"failed at {rep.when}")


# --- Modify json report to include screenshots ---
def pytest_json_modifyreport(json_report: Dict[str, Any]) -> None:
    inject_screenshots(json_report)


# --- Fixtures ---
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    # Set current nodeid so helpers can attach without passing it around
    set_current_nodeid(item.nodeid)


# --- Collection ordering (delegates to src.framework.order) ---
def pytest_collection_modifyitems(config: pytest.Config, items):
    ord.apply_collection_order(config, items)


@pytest.fixture(scope="session")
def capabilities(pytestconfig: pytest.Config) -> Dict[str, Any]:
    key = pytestconfig.getoption("--profile")
    if not key:
        raise pytest.UsageError("You must specify --profile with a key from properties.yml")
    data = cf.load_properties()
    try:
        caps = cf.get_caps_by_key(data, key)
    except KeyError as e:
        raise pytest.UsageError(str(e))
    # Validate browserName with a shared helper
    if cf.get_browser_name(caps) == "unknown":
        raise pytest.UsageError("capabilities is missing or unsupported browserName")
    return caps


@pytest.fixture(scope="session")
def driver(pytestconfig: pytest.Config, capabilities: Dict[str, Any]):
    remote_address = pytestconfig.getoption("--remote-address") or None
    # Inject session-level global for non-pytest contexts
    cf.set_global_driver_type(capabilities)
    setattr(pytestconfig, "_driver_type", cf.get_global_driver_type())
    setattr(pytestconfig, "_remote_address", remote_address)
    # Inject Selenium Grid 4 video capability when requested
    if remote_address and cf.is_video(pytestconfig) and not cf.is_appium_caps(capabilities):
        capabilities["ctm:video-capture"] = "y"

    drv = driver_factory.create_driver(capabilities, remote_address)
    drv.implicitly_wait(30)
    # Session-level reference for screenshots when funcargs are unavailable
    setattr(pytestconfig, "_session_driver", drv)

    # Delegate video start logic (after driver creation)
    start_video_if_enabled(pytestconfig, drv)

    yield drv
    # Delegate video stop logic (before quitting driver)
    quit_driver(pytestconfig, drv)


def quit_driver(pytestconfig: pytest.Config, driver):
    if cf.is_mobile():
        stop_video_if_enabled(pytestconfig)
        driver.quit()
    else:
        driver.quit()
        if getattr(pytestconfig, "_remote_address", None):
            time.sleep(3)
        stop_video_if_enabled(pytestconfig)


@pytest.fixture(scope="function")
def acts(pytestconfig: pytest.Config, driver):
    """Initialize WebActions wrapper for tests."""    
    return WebActions(driver)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int):
    config = session.config
    try:
        from .pdf_report import generate_pdf_report
        html = getattr(config.option, "htmlpath", None)
        json = getattr(config.option, "json_report_file", None)
        out = generate_pdf_report(html_path=html, json_path=json)
        try:
            print(str(out))
        except Exception:
            pass
    except Exception as e:
        try:
            from .pdf_report import generate_pdf_report
            out = generate_pdf_report()
            try:
                print(str(out))
            except Exception:
                pass
        except Exception:
            try:
                print(f"PDF generation failed: {e}")
            except Exception:
                pass


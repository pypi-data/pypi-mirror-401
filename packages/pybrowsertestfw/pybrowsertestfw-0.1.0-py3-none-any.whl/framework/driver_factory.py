from typing import Any, Dict, Optional
import platform

from appium.options.common import AppiumOptions
from appium.webdriver.appium_connection import AppiumConnection
from .config import get_browser_name
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.client_config import ClientConfig
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.safari.options import Options as SafariOptions

from . import config

try:
    # Appium is optional; only required for mobile/webview
    from appium import webdriver as appium_webdriver
except Exception:
    appium_webdriver = None


def _build_chrome_options(caps: Dict[str, Any]) -> ChromeOptions:
    opts = ChromeOptions()
    vendor = caps.get("goog:chromeOptions", {})
    for arg in vendor.get("args", []):
        opts.add_argument(arg)
    exp = vendor.get("experimentalOptions", {})
    for k, v in exp.items():
        opts.add_experimental_option(k, v)
    binary = vendor.get("binary")
    if binary:
        opts.binary_location = binary
    # copy generic capabilities    
    for k, v in caps.items():
        if k in {"browserName", "goog:chromeOptions", "executable_path"}:
            continue
        opts.set_capability(k, v)
    return opts


def _build_edge_options(caps: Dict[str, Any]) -> EdgeOptions:
    opts = EdgeOptions()
    vendor = caps.get("ms:edgeOptions", {})
    for arg in vendor.get("args", []):
        opts.add_argument(arg)
    exp = vendor.get("experimentalOptions", {})
    for k, v in exp.items():
        opts.add_experimental_option(k, v)
    binary = vendor.get("binary")
    if binary:
        opts.binary_location = binary
    for k, v in caps.items():
        if k in {"browserName", "ms:edgeOptions", "executable_path"}:
            continue
        opts.set_capability(k, v)
    return opts


def _build_firefox_options(caps: Dict[str, Any]) -> FirefoxOptions:
    opts = FirefoxOptions()
    vendor = caps.get("moz:firefoxOptions", {})
    for arg in vendor.get("args", []):
        opts.add_argument(arg)
    prefs = vendor.get("prefs", {})
    # binary location can be under vendor or at top
    binary = vendor.get("binary")
    if binary:
        opts.binary_location = binary
    for k, v in prefs.items():
        # set_preference expects str/int/bool
        opts.set_preference(k, v)
    for k, v in caps.items():
        if k in {"browserName", "moz:firefoxOptions", "executable_path", "prefs"}:
            continue
        opts.set_capability(k, v)
    return opts


def _build_safari_options(caps: Dict[str, Any]) -> SafariOptions:
    opts = SafariOptions()
    for k, v in caps.items():
        if k == "browserName":
            continue
        opts.set_capability(k, v)
    return opts


def _build_appium_options(caps: Dict[str, Any]) -> Dict[str, Any]:
    normalized_caps = dict(caps) if caps is not None else {}
    vendor = normalized_caps.get("goog:chromeOptions", {})
    chrome_opts: Dict[str, Any] = {}
    # Args flatten
    if isinstance(vendor.get("args"), list):
        chrome_opts["args"] = vendor.get("args")
    # ExperimentalOptions flatten
    exp = vendor.get("experimentalOptions", {})
    for k, val in exp.items():
        chrome_opts[k] = val
    # Preserve any other existing vendor keys unchanged
    for k, val in vendor.items():
        if k not in ("args", "binary_location", "experimentalOptions"):
            chrome_opts.setdefault(k, val)
    normalized_caps["goog:chromeOptions"] = chrome_opts
    # Return normalized caps
    return normalized_caps


def _assert_local_compatibility(browser_name: str) -> None:
    sys_name = platform.system()
    if browser_name.lower() == "safari" and sys_name != "Darwin":
        raise RuntimeError("Local Safari is only supported on macOS; Windows/Linux are not supported")


def create_driver(caps: Dict[str, Any], remote_address: Optional[str] = None):
    # Normalize and validate capabilities
    browser = get_browser_name(caps)
    if browser == "unknown":
        raise RuntimeError("capabilities is missing or unsupported browserName")

    is_appium = config.is_appium_caps(caps)

    # Local mode: disallow Appium; Safari only on macOS
    if not remote_address:
        if is_appium:
            raise RuntimeError("Appium detected in local mode; provide --remote-address for Appium use")
        _assert_local_compatibility(browser)

        # Local factory mapping
        exec_path = caps.get("executable_path")
        local_factories = {
            "chrome": lambda: webdriver.Chrome(
                service=ChromeService(executable_path=exec_path) if exec_path else ChromeService(),
                options=_build_chrome_options(caps),
            ),
            "edge": lambda: webdriver.Edge(
                service=EdgeService(executable_path=exec_path) if exec_path else EdgeService(),
                options=_build_edge_options(caps),
            ),
            "firefox": lambda: webdriver.Firefox(
                service=FirefoxService(executable_path=exec_path) if exec_path else FirefoxService(),
                options=_build_firefox_options(caps),
            ),
            "safari": lambda: webdriver.Safari(
                options=_build_safari_options(caps)
            ),
        }
        factory = local_factories.get(browser)
        if not factory:
            raise RuntimeError(f"Unsupported local browser: {browser}")
        return factory()

    # Remote mode: Appium or Selenium Grid
    if is_appium:
        return create_appium(caps, remote_address)

    # Selenium Remote mapping
    return create_remote_hub(caps, remote_address, browser)


def create_remote_hub(caps: Dict[str, Any], remote_address: str, browser: str):
    connection = RemoteConnection(
        client_config=ClientConfig(remote_server_addr=remote_address, timeout=1000)
    )
    # Match builders
    remote_builders = {
        "chrome": _build_chrome_options,
        "edge": _build_edge_options,
        "firefox": _build_firefox_options,
        "safari": _build_safari_options,
    }
    builder = remote_builders.get(browser)
    if builder is None:
        raise RuntimeError(f"Unsupported remote browser: {browser}")
    # Create remote webdriver
    opts = builder(caps)
    return webdriver.Remote(command_executor=connection, options=opts)


def create_appium(caps: Dict[str, Any], remote_address: str):
    connection = AppiumConnection(
        client_config=ClientConfig(remote_server_addr=remote_address, timeout=1000),
    )
    # Create appium driver
    if appium_webdriver is None:
        raise RuntimeError("appium-python-client is not installed; cannot create Appium session")
    # Build Appium options
    normalized_caps = _build_appium_options(caps)
    options = AppiumOptions()
    options.load_capabilities(normalized_caps)
    return appium_webdriver.Remote(command_executor=connection, options=options)


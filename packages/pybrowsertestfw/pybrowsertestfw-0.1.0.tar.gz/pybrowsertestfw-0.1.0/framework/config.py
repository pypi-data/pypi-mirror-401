import os
from typing import Any, Dict

import pytest
import yaml

DEFAULT_PROPERTIES_PATH = os.path.join(os.getcwd(), "properties.yml")

# Session-level global driver_type (set by plugin at session start)
_GLOBAL_DRIVER_TYPE: str = "unknown"


def load_properties(path: str = DEFAULT_PROPERTIES_PATH) -> Dict[str, Any]:
    """Load properties.yml.
    Default path: project root /properties.yml.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("Invalid properties.yml: top-level must be a dict (key-value)")
    return data


def get_caps_by_key(data: Dict[str, Any], key: str) -> Dict[str, Any]:
    caps = data.get(key)
    if caps is None:
        raise KeyError(f"Key not found in properties.yml: {key}")
    if not isinstance(caps, dict):
        raise ValueError(f"Value for key '{key}' must be a dict")
    return caps


# Common: parse and normalize browser name from capabilities
# Returns: chrome | edge | firefox | safari | unknown
def get_browser_name(caps: Dict[str, Any]) -> str:
    raw = str(caps.get("browserName") or "").strip().lower()
    if not raw:
        return "unknown"
    if raw in ("edge", "msedge", "microsoftedge", "microsoft edge"):
        return "edge"
    if raw in ("chrome", "googlechrome", "google chrome"):
        return "chrome"
    if raw in ("firefox", "mozilla firefox", "mozillafirefox"):
        return "firefox"
    if raw == "safari":
        return "safari"
    return "unknown"


# --- Runtime read-only global APIs (injected by plugin at session start) ---
def set_global_driver_type(caps: Dict[str, Any]) -> None:
    """Set the session-global driver_type (lowercase)."""
    global _GLOBAL_DRIVER_TYPE
    # Appium: use platformName (Android/iOS); Web: use browserName
    _GLOBAL_DRIVER_TYPE = caps.get("platformName", "mobile").lower() if is_appium_caps(caps) else get_browser_name(caps).lower()


def get_global_driver_type() -> str:
    """Get the session-global driver_type."""
    return _GLOBAL_DRIVER_TYPE


def is_mobile() -> bool:
    """Determine mobile based on global driver_type."""
    return get_global_driver_type().lower() in ("android", "ios")


def is_video(pytestconfig: pytest.Config) -> bool:
    """Determine if video recording is enabled."""
    video_opt = str(pytestconfig.getoption("--video") or "n").lower()
    return True if video_opt == "y" else False


def is_appium_caps(caps: Dict[str, Any]) -> bool:
    return (
        "automationName" in caps or "appium:automationName" in caps
        or any(k.startswith("appium:") for k in caps.keys())
    )


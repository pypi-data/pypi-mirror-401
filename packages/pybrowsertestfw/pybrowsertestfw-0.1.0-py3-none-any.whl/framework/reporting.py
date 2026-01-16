import os
import time
import base64
from typing import Any, Dict, List, Tuple, Optional
import threading

import pytest

# Project root for reports and artifacts
PROJECT_ROOT = os.getcwd()

# Global screenshot index for json report
_SCREENSHOT_INDEX: Dict[str, List[str]] = {}

# Pending HTML extras to attach per nodeid: list of (png_bytes, fname, label)
_PENDING_EXTRAS: Dict[str, List[Tuple[bytes, str, str]]] = {}

# Global config and current test context (thread-local)
_GLOBAL_CONFIG: Optional[pytest.Config] = None
_TL = threading.local()


def set_global_config(config: pytest.Config) -> None:
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = config


def set_current_nodeid(nodeid: str) -> None:
    try:
        _TL.nodeid = nodeid
    except Exception:
        pass


def get_current_nodeid() -> str:
    return getattr(_TL, "nodeid", "case")


# --- Naming helpers ---
def now_str() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def safe_name(nodeid: str) -> str:
    return (
        nodeid.replace("/", "_")
        .replace("::", "_")
        .replace(" ", "_")
        .replace("[", "_")
        .replace("]", "_")
    )


def init_reporting(config: pytest.Config):
    """Initialize reports dir and screenshot dir; configure html/json outputs.
    Returns (reports_dir, screenshot_dir, ts).
    """
    reports_root = os.path.join(PROJECT_ROOT, "reports")
    os.makedirs(reports_root, exist_ok=True)

    # Use existing timestamp if already set early; else create one
    ts = getattr(config, "_report_ts", None) or now_str()
    setattr(config, "_report_ts", ts)

    reports_dir = os.path.join(reports_root, ts)
    os.makedirs(reports_dir, exist_ok=True)

    screenshot_dir = os.path.join(reports_dir, "screenshot")
    os.makedirs(screenshot_dir, exist_ok=True)

    # store on config for global access
    setattr(config, "_reports_dir", reports_dir)
    setattr(config, "_screenshot_dir", screenshot_dir)
    # Ensure global access for simplified helpers
    set_global_config(config)

    # pytest-html
    html_path = getattr(config.option, "htmlpath", None)
    if not html_path:
        setattr(config.option, "htmlpath", os.path.join(reports_dir, f"report_{ts}.html"))
        setattr(config.option, "self_contained_html", True)

    # pytest-json-report: enable and force path to reports/<ts>/report_<ts>.json
    try:
        setattr(config.option, "json_report", True)
    except Exception:
        pass
    try:
        json_target = os.path.join(reports_dir, f"report_{ts}.json")
        setattr(config.option, "json_report_file", json_target)
    except Exception:
        pass

    # pytest-pdf fallback at process exit to avoid missing sessionfinish
    try:
        import atexit
        from .pdf_report import generate_pdf_report

        def _gen_pdf_at_exit():
            try:
                html = getattr(config.option, "htmlpath", None)
                json = getattr(config.option, "json_report_file", None)
                generate_pdf_report(html_path=html, json_path=json)
            except Exception:
                try:
                    generate_pdf_report()
                except Exception:
                    pass

        atexit.register(_gen_pdf_at_exit)
    except Exception:
        pass

    return reports_dir, screenshot_dir, ts

# --- Reporting helpers (single source of truth) ---
def get_reports_dir(config: pytest.Config) -> str:
    rd = getattr(config, "_reports_dir", None)
    if rd:
        return rd
    reports_root = os.path.join(PROJECT_ROOT, "reports")
    os.makedirs(reports_root, exist_ok=True)
    ts = getattr(config, "_report_ts", None) or now_str()
    rd = os.path.join(reports_root, ts)
    os.makedirs(rd, exist_ok=True)
    setattr(config, "_reports_dir", rd)
    return rd


def get_report_ts(config: pytest.Config) -> str:
    ts = getattr(config, "_report_ts", None)
    if ts:
        return ts
    ts = now_str()
    setattr(config, "_report_ts", ts)
    return ts


def build_artifact_path(config: pytest.Config, name: str, ext: str) -> str:
    """Build a path inside reports/<ts> for an artifact (e.g., video/log)."""
    rd = get_reports_dir(config)
    ts = get_report_ts(config)
    return os.path.join(rd, f"{name}_{ts}.{ext}")


def get_screenshot_dir(config: pytest.Config) -> str:
    """Return screenshot dir inside current reports run, initialize if missing."""
    sdir = getattr(config, "_screenshot_dir", None)
    if sdir:
        return sdir
    rd = get_reports_dir(config)
    sdir = os.path.join(rd, "screenshot")
    os.makedirs(sdir, exist_ok=True)
    setattr(config, "_screenshot_dir", sdir)
    return sdir


def build_screenshot_path(config: pytest.Config) -> str:
    """Build ss_{now}.png inside screenshot dir. Nodeid excluded for brevity."""
    ts = now_str()
    file_name = f"ss_{ts}.png"
    screenshot_dir = get_screenshot_dir(config)
    return os.path.join(screenshot_dir, file_name)


def attach_to_html(config: pytest.Config, rep: pytest.TestReport, png_bytes: bytes, fname: str, label: str) -> None:
    """Attach screenshot to pytest-html report as inline image."""
    try:
        pytest_html = config.pluginmanager.getplugin("html")
        if not pytest_html:
            return
        b64 = base64.b64encode(png_bytes).decode("ascii")
        image_extra = pytest_html.extras.image(b64, mime_type="image/png")
        label_extra = pytest_html.extras.html(f"<div><strong>{label}</strong>: {fname}</div>")
        # Prefer new 'extras' API; avoid deprecated 'extra'
        if hasattr(rep, "extras") and rep.extras:
            rep.extras.extend([label_extra, image_extra])
        else:
            rep.extras = [label_extra, image_extra]
    except Exception:
        pass


def record_json(nodeid: str, path: str) -> None:
    """Record screenshot path relative to project root for json report."""
    try:
        rel_path = os.path.relpath(path, PROJECT_ROOT)
        _SCREENSHOT_INDEX.setdefault(nodeid, []).append(rel_path)
    except Exception:
        pass


def capture_and_attach(config: pytest.Config, rep: pytest.TestReport, driver, label: str) -> None:
    """Capture, save, attach to HTML, and record to JSON index."""
    try:
        nodeid = getattr(rep, "nodeid", "case")
        path = build_screenshot_path(config)
        fname = os.path.basename(path)
        png = driver.get_screenshot_as_png()
        try:
            with open(path, "wb") as f:
                f.write(png)
        except Exception:
            pass
        attach_to_html(config, rep, png, fname, label)
        record_json(nodeid, path)
    except Exception:
        pass


def capture_and_queue_simple(driver) -> str:
    """Capture from driver and save+queue with default label."""
    config = _GLOBAL_CONFIG
    if not config:
        return ""
    try:
        png = driver.get_screenshot_as_png()
    except Exception:
        return ""
    node_id = get_current_nodeid()
    path = build_screenshot_path(config)
    file_name = os.path.basename(path)
    try:
        with open(path, "wb") as f:
            f.write(png)
    except Exception:
        pass
    try:
        _PENDING_EXTRAS.setdefault(node_id, []).append((png, file_name, "manual"))
    except Exception:
        pass
    record_json(node_id, path)
    return path


def drain_pending_extras(config: pytest.Config, rep: pytest.TestReport) -> None:
    """Attach all queued screenshots for the current test to HTML and clear queue."""
    try:
        nodeid = getattr(rep, "nodeid", "case")
        pending = _PENDING_EXTRAS.pop(nodeid, [])
        for png, fname, label in pending:
            attach_to_html(config, rep, png, fname, label)
    except Exception:
        pass

# --- Json report hook helper ---
def inject_screenshots(json_report: Dict[str, Any]) -> None:
    """Inject screenshots field into each test item in json report."""
    try:
        tests = json_report.get("tests", [])
        for t in tests:
            nodeid = t.get("nodeid")
            if nodeid and nodeid in _SCREENSHOT_INDEX:
                t["screenshots"] = _SCREENSHOT_INDEX.get(nodeid, [])
    except Exception:
        pass


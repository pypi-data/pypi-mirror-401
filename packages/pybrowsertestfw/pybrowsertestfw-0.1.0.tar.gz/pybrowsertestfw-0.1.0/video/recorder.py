import base64
import os
from typing import Optional
from framework.config import is_mobile, is_video
import pytest
from framework.reporting import build_artifact_path
from framework.logger import get_logger
from urllib import request


logger = get_logger("video.recorder")


class BaseVideoRecorder:
    def __init__(self, driver=None, remote_address: Optional[str] = None):
        self.driver = driver
        self.remote_address = remote_address
        self.output_path: Optional[str] = None

    def start(self, output_path: str):
        self.output_path = output_path

    def stop(self):
        pass


class SeleniumVideoRecorder(BaseVideoRecorder):
    def __init__(self, driver=None, remote_address: Optional[str] = None):
        super().__init__(driver, remote_address)
        self._recorder = None
        self._started = False

    def _full_screen_region(self):
        """Return primary monitor full-screen region via screeninfo.
        If unavailable, return None and let caller decide.
        """
        try:
            from screeninfo import get_monitors
            mons = get_monitors()
            if mons:
                primary = next((m for m in mons if getattr(m, "is_primary", False)), mons[0])
                return {"mon": 1, "left": 0, "top": 0, "width": int(primary.width), "height": int(primary.height)}
        except Exception:
            pass
        return None

    def start(self, output_path: str):
        super().start(output_path)
        try:
            from .pyscreenrec import ScreenRecorder  # use local implementation
        except Exception as e:
            logger.error(f"Video recording disabled: local pyscreenrec import failed: {e}")
            return

        region = self._full_screen_region()
        if not region:
            logger.error("Video recording disabled: cannot determine screen region via screeninfo.")
            return

        try:
            # Ensure output directory exists only when we actually record
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Initialize recorder and start full-screen capture
            self._recorder = ScreenRecorder()
            self._recorder.start_recording(output_path, 24, region)
            self._started = True
        except Exception as e:
            logger.error(f"Video recording failed to start: {e}")
            self._recorder = None
            self._started = False

    def stop(self):
        try:
            if self._recorder and self._started:
                self._recorder.stop_recording()
                self._started = False
        except Exception as e:
            logger.error(f"Video recording failed to stop: {e}")


class SeleniumRemoteRecorder(BaseVideoRecorder):
    def __init__(self, driver=None, remote_address: Optional[str] = None):
        super().__init__(driver, remote_address)
        self._video_url: Optional[str] = None

    def _build_video_url(self) -> Optional[str]:
        if not self.driver:
            return None
        session_id = getattr(self.driver, "session_id", None)
        base = self.remote_address
        if not session_id or not base:
            return None
        # Replace /wd/hub -> /se/grid/hub/videoCache/
        if "/wd/hub" in base:
            base = base.replace("/wd/hub", "/se/grid/hub/videoCache/")
        else:
            base = base.rstrip("/") + "/se/grid/hub/videoCache/"
        return base + str(session_id)

    def start(self, output_path: str):
        super().start(output_path)
        self._video_url = self._build_video_url()
        logger.info(f"Remote video url prepared: {self._video_url}")

    def stop(self):
        try:
            if not self._video_url or not self.output_path:
                return
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            req = request.Request(self._video_url, method="GET")
            with request.urlopen(req, timeout=900) as resp:
                data = resp.read()
                with open(self.output_path, "wb") as f:
                    f.write(data)
            logger.info(f"Remote video saved: {self.output_path}")
        except Exception as e:
            logger.error(f"Remote video fetch failed: {e}")


class AppiumVideoRecorder(BaseVideoRecorder):
    def start(self, output_path: str):
        super().start(output_path)
        # Start Appium recording if driver supports it
        try:
            if self.driver and hasattr(self.driver, "start_recording_screen"):
                self.driver.start_recording_screen()
                logger.info("Appium screen recording started.")
        except Exception:
            # Fail silently to avoid impacting test flow
            pass

    def stop(self):
        # Stop recording and save to file
        try:
            if self.driver and hasattr(self.driver, "stop_recording_screen") and self.output_path:
                encoded = self.driver.stop_recording_screen()
                # Appium returns base64 string
                if isinstance(encoded, bytes):
                    encoded = encoded.decode("utf-8", errors="ignore")
                data = base64.b64decode(encoded)
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                with open(self.output_path, "wb") as f:
                    f.write(data)
                logger.info(f"Appium screen recording saved: {self.output_path}")
        except Exception:
            pass


def create_recorder(driver, remote_address: Optional[str] = None):
    if is_mobile():
        logger.info("Mobile device detected, using Appium video recorder.")
        return AppiumVideoRecorder(driver)
    if remote_address:
        logger.info(f"Remote address detected: {remote_address}, using Selenium Grid 4 video recorder.")
        return SeleniumRemoteRecorder(driver, remote_address)
    logger.info("No remote address detected, using local Selenium video recorder.")
    return SeleniumVideoRecorder(driver)


def start_video_if_enabled(pytestconfig: pytest.Config, driver) -> None:
    """Called after driver creation: enable recording based on --video.
    - Handle video logic and path calculation only, keep plugin clean.
    """
    if not is_video(pytestconfig):
        return

    try:
        remote_address = getattr(pytestconfig, "_remote_address", None)
        video_path = build_artifact_path(pytestconfig, "video", "mp4")
        recorder = create_recorder(driver, remote_address)
        recorder.start(video_path)
        setattr(pytestconfig, "_video_recorder", recorder)
    except Exception:
        # Silent recording errors to avoid breaking tests
        pass


def stop_video_if_enabled(pytestconfig: pytest.Config) -> None:
    """Called before driver quits: stop and save if recording was started."""
    try:
        recorder = getattr(pytestconfig, "_video_recorder", None)
        if recorder:
            recorder.stop()
    except Exception:
        pass

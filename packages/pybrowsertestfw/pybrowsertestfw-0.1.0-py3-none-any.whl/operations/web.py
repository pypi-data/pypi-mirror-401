from selenium.common import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from framework import config, reporting
from framework.logger import get_logger
import os
import csv


class WebActions:
    def __init__(self, driver: WebDriver, default_timeout: int = 30):
        self.driver = driver
        self.wait = WebDriverWait(driver, default_timeout)
        self.driver_type = config.get_global_driver_type()
        self.logger = get_logger("operations.web")
        self.accept_next_alert = True

    def is_mobile(self) -> bool:
        return config.is_mobile()

    def screenshot(self) -> None:
        """Capture screenshot and enqueue default attachment to report."""
        try:
            reporting.capture_and_queue_simple(self.driver)
            self.logger.info("screenshot saved and queued")
        except Exception as e:
            self.logger.error(f"screenshot capture failed: {e}")
            pass

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            alert = self.driver.switch_to.alert
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def load_vars_from_csv(self, file_name: str, data_dir: str = "datas"):
        base = (file_name or "").strip()
        if not base:
            raise ValueError("file_name is required")
        csv_path = os.path.join(os.getcwd(), data_dir, base)
        rows: list[dict[str, str]] = []
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows


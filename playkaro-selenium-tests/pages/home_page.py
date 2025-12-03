# pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HomePage:
    def __init__(self, driver, base_url="https://playkaroproject.netlify.app/"):
        self.driver = driver
        self.base_url = base_url

    def open(self, path="/"):
        # open the app root or the provided path
        url = self.base_url.rstrip("/") + path
        self.driver.get(url)

    def _wait_for_any(self, timeout, locator):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return None

    def get_logo_element(self, timeout=5):
        # Try multiple fallbacks but do not raise. Return None if not found.
        tries = [
            (By.XPATH, "//header//a[.//text()[contains(., 'PlayKaro')]]"),
            (By.XPATH, "//*[contains(text(), 'PlayKaro')]"),
            (By.CSS_SELECTOR, "header a"),
            (By.CSS_SELECTOR, "img[alt*='PlayKaro']"),
            (By.CSS_SELECTOR, ".logo, .brand"),
        ]
        for by, selector in tries:
            el = self._wait_for_any(timeout, (by, selector))
            if el:
                try:
                    if el.is_displayed():
                        return el
                    # return non-visible candidate for debugging
                    return el
                except Exception:
                    return el
        return None

    def get_sign_in_button(self, timeout=5):
        tries = [
            (By.CSS_SELECTOR, "a[href*='/auth'] button"),
            (By.CSS_SELECTOR, "button:contains('Sign In')"),
            (By.XPATH, "//button[contains(., 'Sign In')]"),
            (By.CSS_SELECTOR, "a[href*='auth']"),
        ]
        for by, selector in tries:
            el = self._wait_for_any(timeout, (by, selector))
            if el:
                return el
        return None

    def get_all_video_cards(self, timeout=8):
        # Wait for loading spinner to disappear or for cards to appear
        # Common class used in many UIs: '.video-card' . Change as needed.
        cards_selector_candidates = [
            (By.CSS_SELECTOR, ".video-card"),
            (By.CSS_SELECTOR, ".card"),
            (By.CSS_SELECTOR, "[data-video-card]"),
            (By.CSS_SELECTOR, ".video, .media-card"),
        ]
        # first wait a little for dynamic load
        end_time = time.time() + timeout
        while time.time() < end_time:
            for by, sel in cards_selector_candidates:
                els = self.driver.find_elements(by, sel)
                if els:
                    return els
            # also allow JS-driven loading: give small sleep
            time.sleep(0.5)
        return []

    def click_first_video_card(self):
        cards = self.get_all_video_cards()
        if not cards:
            # return False to indicate not found instead of raising
            return False
        try:
            cards[0].click()
            return True
        except Exception:
            # attempt JS click as fallback
            try:
                self.driver.execute_script("arguments[0].click();", cards[0])
                return True
            except Exception:
                return False

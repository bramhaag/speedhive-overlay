from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class Scraper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://speedhive.mylaps.com/LiveTiming")
        self._accept_cookies()
        self.stage = "start"

    def get_results(self):
        if self.stage == "start":
            self._select_event()

        if self.stage == "event":
            self._select_session()

        if self.stage == "session":
            if "finish-flag" == self._get_status():
                self._back_to_event()
                self._select_session()
                if self.stage != "session":
                    print("Attempt to switch session unsuccessful")
                    return {}
                print("Switched session successfully")

            return self._parse_session()

        print("No session found: ", self.stage)
        return {}

    def _accept_cookies(self):
        self.driver.switch_to.frame(self._wait_and_get("#gdpr-consent-notice"))
        self._wait_and_get('#save').click()

        # Accept other cookie banner
        self._wait_and_get("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()

    def _select_event(self):
        events = self._wait_and_get_all(".live-events > .col-xs-12 > a")
        for e in events:
            name = e.find_element(By.CSS_SELECTOR, ".event-details > .event-name")
            location = e.find_element(By.CSS_SELECTOR, ".event-details > .event-extra > .event-location")

            if "gggggg" in name.text.lower() or "oldenzaal" in location.text.lower():
                e.click()
                self.stage = "event"
                return

        print("No event found")

    def _back_to_event(self):
        self._wait_and_get("#breadcrumb > div > div > ul > li > a:last-of-type").click()
        self.stage = "event"

    def _select_session(self):
        try:
            self._get_element("a.row-session.green-session").click()
            self.stage = "session"
        except Exception:
            pass

    def _get_status(self):
        try:
            return self._get_element("#flag-status").get_attribute("class")
        except Exception:
            return None

    def _parse_session(self):
        results = [{
            "name": element.find_element(By.CSS_SELECTOR, "div.competitor").text,
            "pos": element.find_element(By.CSS_SELECTOR, "div.position > span.value").text,
            "last": element.find_element(By.CSS_SELECTOR, "div.last-time").text,
            "diff": element.find_element(By.CSS_SELECTOR, "div.diff").text
        } for element in self._get_elements("#result-list > div.results-list > div.row-result")]

        return {
            "session": self._get_element("#session-name > span:nth-child(2)").text,
            "time": self._get_element("#session-time").text,
            "results": results
        }

    def _wait_and_get_all(self, selector, wait=15):
        if wait > 0:
            WebDriverWait(self.driver, wait).until(ec.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return self._get_elements(selector)

    def _wait_and_get(self, selector, wait=15):
        if wait > 0:
            WebDriverWait(self.driver, wait).until(ec.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return self._get_element(selector)

    def _get_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def _get_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def _get_text(self, selector):
        return self._get_element(selector).text

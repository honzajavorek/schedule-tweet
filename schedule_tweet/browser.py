import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger('schedule_tweet.browser')


class Browser():
    def __init__(self, driver):
        self.driver = driver or webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 5)

    def load(self, url):
        logger.debug(f'load {url}')
        self.driver.get(url)

    def _when_visible(self, css_selector):
        locator = (By.CSS_SELECTOR, css_selector)
        condition = expected_conditions.visibility_of_element_located(locator)
        return self.wait.until(condition)

    def _when_visible_all(self, css_selector):
        self._when_visible(css_selector)
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)

    def _when_clickable(self, css_selector):
        locator = (By.CSS_SELECTOR, css_selector)
        condition = expected_conditions.element_to_be_clickable(locator)
        return self.wait.until(condition)

    def find(self, css_selector):
        logger.debug(f'find {css_selector}')
        return self._when_visible(css_selector)

    def find_all(self, css_selector):
        logger.debug(f'find_all {css_selector}')
        return self._when_visible_all(css_selector)

    def title_all(self, css_selector):
        logger.debug(f'title_all {css_selector}')
        return [
            element.get_attribute('title').strip() for element
            in self._when_visible_all(css_selector)
        ]

    def count(self, css_selector):
        logger.debug(f'count {css_selector}')
        return len(self._when_visible_all(css_selector))

    def text(self, css_selector):
        logger.debug(f'text {css_selector}')
        return self._when_visible(css_selector).text.strip()

    def is_visible(self, css_selector):
        logger.debug(f'is_visible {css_selector}')
        try:
            return bool(self._when_visible(css_selector))
        except:
            return False

    def click(self, css_selector):
        logger.debug(f'click {css_selector}')
        self._when_clickable(css_selector).click()

    def fill(self, css_selector, text):
        logger.debug(f'fill {css_selector} ({len(text)} characters)')
        element = self._when_clickable(css_selector)
        element.clear()
        element.send_keys(text)

    def value(self, css_selector):
        logger.debug(f'value {css_selector}')
        return self._when_clickable(css_selector).get_attribute('value').strip()

    def submit(self, css_selector):
        logger.debug(f'submit {css_selector}')
        element = self._when_clickable(css_selector)
        element.submit()

    def scroll_to(self, css_selector):
        logger.debug(f'scroll_to {css_selector}')
        self.driver.execute_script(f'document.querySelector("{css_selector}").scrollIntoView()')

    def save_screenshot(self, path):
        logger.debug(f'save_screenshot {path}')
        self.driver.save_screenshot(path)

    def quit(self, screenshot_file=None):
        with_screenshot = f'(screenshot: {screenshot_file})' if screenshot_file else ''
        logger.debug(f'quit {with_screenshot}')
        try:
            if screenshot_file:
                self.driver.save_screenshot(screenshot_file)
            self.driver.quit()
        except:
            pass

import os
import logging

from schedule_tweet.browser import Browser
from schedule_tweet.page_objects import landing_page, login_page, app_page


__all__ = ('Session', 'session')


logger = logging.getLogger('schedule_tweet.session')


class Session():
    def __init__(self, username, password, phone=None, driver=None,
                 screenshot_file=None):
        self.browser = Browser(driver)

        self.username = username.lstrip('@')
        self.password = password
        self.phone = phone

        self.screenshot_file = (
            screenshot_file or
            os.getenv('SCREENSHOT_FILE') or
            os.path.join(os.getcwd(), 'error.png')
        )

    def open(self):
        try:
            logger.info('loading')
            landing_page.load(self.browser)

            logger.info('logging in')
            landing_page.go_to_login_page(self.browser)
            login_page.login(self.browser, self.username, self.password)

            logger.info('verifying phone number')
            login_page.verify_phone(self.browser, self.phone)

            logger.info('opening left pane')
            app_page.open_left_pane(self.browser)

            logger.info(f'selecting account: {self.username}')
            app_page.select_account(self.browser, self.username)
        except Exception:
            self.browser.quit(self.screenshot_file)
            raise

    def tweet(self, dt, text):
        try:
            logger.info('filling tweet text')
            app_page.fill_tweet_text(self.browser, text)

            logger.info('opening calendar widget')
            app_page.open_calendar(self.browser)

            logger.info(f'setting date & time to {dt.isoformat()}')
            app_page.set_datetime(self.browser, dt)

            logger.info('sending tweet')
            app_page.send_tweet(self.browser)
        except Exception:
            self.browser.quit(self.screenshot_file)
            raise

    def close(self):
        self.browser.quit()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc, *args):
        self.close()


session = Session

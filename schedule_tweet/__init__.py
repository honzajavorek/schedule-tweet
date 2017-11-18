import os
import logging
from datetime import datetime, timedelta

from schedule_tweet.browser import Browser
from schedule_tweet.page_objects import landing_page, login_page, app_page


__all__ = ('Session', 'session')


logger = logging.getLogger('schedule_tweet.session')


class Session():
    def __init__(self, username, password, phone=None, driver=None, screenshot_file=None):
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
        browser = self.browser
        try:
            logger.info('loading')
            browser.load('https://tweetdeck.twitter.com/')
            browser.click(landing_page.login_button)

            logger.info('logging in')
            browser.fill(login_page.form_username, self.username)
            while not browser.value(login_page.form_password):
                browser.fill(login_page.form_password, self.password)
            browser.submit(login_page.form)

            logger.info('verifying phone number')
            if browser.is_visible(login_page.form_phone):
                if self.phone:
                    browser.fill(login_page.form_phone, self.phone)
                    browser.submit(login_page.form_phone)
                else:
                    raise Exception('TweetDeck login prompted for phone number, but none was provided')
            else:
                logger.info('no phone number verification needed')

            logger.info('opening left pane')
            browser.find(app_page.left_pane)
            if browser.is_visible(app_page.left_pane_open_button):
                browser.click(app_page.left_pane_open_button)
                browser.click(app_page.left_pane_remember_state_checkbox)
            else:
                logger.info('left pane is already open')

            account = f'@{self.username}'
            logger.info(f'selecting account: {account}')
            if browser.count(app_page.account_buttons) > 1:
                browser.click(app_page.account_button_selected)
                for title in browser.title_all(app_page.account_buttons):
                    if title.lower() == account:
                        browser.click(app_page.account_button.format(title=title))
        except:
            browser.quit(self.screenshot_file)
            raise

    def tweet(self, dt, text):
        browser = self.browser
        try:
            logger.info('filling tweet text')
            browser.fill(app_page.textarea, text)

            logger.info('checking tweet length')
            if browser.is_visible(app_page.textarea_char_count):
                char_count = browser.text(app_page.textarea_char_count)
                count = int(char_count or 0)
                if count < 0:
                    raise Exception(f'The tweet is too long: {count}')
                else:
                    logger.info('tweet length is OK')
            else:
                logger.info('tweet length is OK')

            logger.info('opening calendar widget')
            browser.click(app_page.calendar_open_button)
            browser.scroll_to(app_page.calendar_bottom)

            hour = str(dt.hour)
            minute = str(dt.minute)
            am_pm = datetime.strftime(dt, '%p')
            logger.info(f'setting time to {hour}:{minute}{am_pm}')
            browser.fill(app_page.calendar_hour_input, hour)
            browser.fill(app_page.calendar_minute_input, minute)
            if browser.text(app_page.calendar_am_pm_button).upper() != am_pm.upper():
                browser.click(app_page.calendar_am_pm_button)

            expected_calendar_title = datetime.strftime(dt, '%B %Y')
            logger.info(f'setting month to {expected_calendar_title}')
            while True:
                calendar_title = browser.text(app_page.calendar_title)
                calendar_title_dt = datetime.strptime(calendar_title, '%B %Y')

                if calendar_title != expected_calendar_title:
                    logger.debug(f'clicking on next month: {calendar_title} (current) ≠ {expected_calendar_title} (expected)')
                    browser.click(app_page.calendar_next_month_button)
                else:
                    logger.debug(f'keeping current month: {calendar_title} (current) = {expected_calendar_title} (expected)')
                    break

            logger.info(f'setting day to {dt.day}')
            browser.click(app_page.calendar_day.format(day=dt.day))

            logger.info(f'verifying date & time')
            schedule_button_label = browser.text(app_page.calendar_open_button_label)

            hour_not_zero_padded = datetime.strftime(dt, '%I').lstrip('0')
            day_not_zero_padded = datetime.strftime(dt, '%d').lstrip('0')
            # example: '4:01 PM · Mon 4 Dec 2017'
            expected_schedule_button_label = datetime.strftime(
                dt,
                f'{hour_not_zero_padded}:%M %p · %a {day_not_zero_padded} %b %Y'
            )
            if schedule_button_label != expected_schedule_button_label:
                raise Exception(f"TweetDeck UI displays '{schedule_button_label}' as the effective date & time, but '{expected_calendar_title}' is expected")
            else:
                logger.debug(f"correct, {schedule_button_label} = {expected_calendar_title}")

            logger.info(f'submitting tweet')
            browser.click(app_page.textarea)
            browser.click(app_page.submit_button)
            browser.click(app_page.textarea)
        except:
            browser.quit(self.screenshot_file)
            raise

    def close(self):
        self.browser.quit()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc, *args):
        self.close()


session = Session

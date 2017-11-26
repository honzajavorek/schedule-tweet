from datetime import datetime


left_pane = '.js-app'
left_pane_open_button = '.js-app button.js-show-drawer'
left_pane_remember_state_checkbox = (
    '.js-app.hide-detail-view-inline .js-compose-stay-open'
)

account_buttons = '.js-app .js-account-item'
account_button = '.js-app .js-account-item[title="{title}"]'
account_button_selected = '.js-app .js-account-item.is-selected'

textarea = '.js-app textarea.js-compose-text'
textarea_char_count = '.js-app .js-character-count'

calendar_open_button = '.js-app .js-schedule-button'
calendar_open_button_label = '.js-app .js-schedule-button-label'

calendar_hour_input = '.js-app .cal #scheduled-hour'
calendar_minute_input = '.js-app .cal #scheduled-minute'
calendar_am_pm_button = '.js-app .cal #amPm'
calendar_next_month_button = '#calendar #next-month'
calendar_title = '.js-app .cal #caltitle'
calendar_day = '.js-app .calweek a[href="#{day}"]:not(.caloff)'
calendar_bottom = '.js-app .js-remove'

send_button = '.js-app .js-send-button'


def open_left_pane(browser):
    browser.find(left_pane)
    if browser.is_visible(left_pane_open_button):
        browser.click(left_pane_open_button)
        browser.click(left_pane_remember_state_checkbox)


def select_account(browser, username):
    account_name = f'@{username}'
    if browser.count(account_buttons) > 1:
        # first, deselect the currently selected one
        browser.click(account_button_selected)

        # find the one we need and click on it
        for title in browser.title_all(account_buttons):
            if title.lower() == account_name:
                browser.click(account_button.format(title=title))


def fill_tweet_text(browser, text):
    browser.fill(textarea, text)

    if browser.is_visible(textarea_char_count):
        char_count = browser.text(textarea_char_count)
        count = int(char_count or 0)
        if count < 0:
            raise Exception(f'The tweet is too long: {count}')


def open_calendar(browser):
    browser.click(calendar_open_button)
    browser.scroll_to(calendar_bottom)


def set_datetime(browser, dt):
    set_time(browser, dt)
    set_date(browser, dt)

    # example: '4:01 PM · Mon 4 Dec 2017'
    current_label = browser.text(calendar_open_button_label)

    hour_not_zero_padded = datetime.strftime(dt, '%I').lstrip('0')
    day_not_zero_padded = datetime.strftime(dt, '%d').lstrip('0')
    format = f'{hour_not_zero_padded}:%M %p · %a {day_not_zero_padded} %b %Y'
    expected_label = datetime.strftime(dt, format)

    if current_label != expected_label:
        raise Exception(
            f"TweetDeck UI displays '{current_label}' as "
            f"the effective date & time, but '{expected_label}'"
            " is expected"
        )


def set_time(browser, dt):
    browser.fill(calendar_hour_input, str(dt.hour))
    browser.fill(calendar_minute_input, str(dt.minute))

    # AM/PM toggle
    am_pm_current = browser.text(calendar_am_pm_button)
    am_pm_expected = datetime.strftime(dt, '%p')
    if am_pm_current.upper() != am_pm_expected.upper():
        browser.click(calendar_am_pm_button)


def set_date(browser, dt):
    expected_calendar_title = datetime.strftime(dt, '%B %Y')
    while True:
        current_calendar_title = browser.text(calendar_title)
        if current_calendar_title != expected_calendar_title:
            browser.click(calendar_next_month_button)
        else:
            break
    browser.click(calendar_day.format(day=dt.day))


def send_tweet(browser):
    browser.click(textarea)
    browser.click(send_button)
    browser.click(textarea)

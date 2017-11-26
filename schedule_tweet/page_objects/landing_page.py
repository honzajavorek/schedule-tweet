login_button = 'form.form-login .btn'


def load(browser):
    browser.load('https://tweetdeck.twitter.com/')


def go_to_login_page(browser):
    browser.click(login_button)

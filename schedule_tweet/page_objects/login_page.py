form = 'form.signin'
form_username = 'form.signin [name="session[username_or_email]"]'
form_password = 'form.signin [name="session[password]"]'
form_phone = '#challenge_response'


def login(browser, username, password):
    browser.fill(form_username, username)

    # For some reason filling of the password is flaky and needs to be
    # repeated until the input really gets the value set
    while not browser.value(form_password):
        browser.fill(form_password, password)

    browser.submit(form)


def verify_phone(browser, phone=None):
    if browser.is_visible(form_phone):
        if phone:
            browser.fill(form_phone, phone)
            browser.submit(form_phone)
        else:
            raise Exception('TweetDeck login prompted for phone '
                            'number, but none was provided')

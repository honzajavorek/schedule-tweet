Schedule Tweet
==============

Automated tweet scheduling using `TweetDeck <http://tweetdeck.twitter.com/>`_. Uses `Selenium <http://docs.seleniumhq.org/>`_ to spawn a browser, log in to TweetDeck with your credentials, and schedule a tweet on your behalf by clicking on things in the app.

Installation
------------

Install `geckodriver <https://github.com/mozilla/geckodriver>`_. On macOS with `Homebrew <http://homebrew.sh/>`_ you can use ``brew install geckodriver``. Then...

.. code-block:: shell

    $ pip install schedule_tweet

Only **Python 3.6** and higher is supported.

Usage
-----

.. code-block:: python

    >>> import os
    >>> from datetime import datetime, timedelta
    >>>
    >>> import schedule_tweet
    >>>
    >>> username = 'schedule_tw'
    >>> password = os.getenv('PASSWORD')
    >>> now_dt = datetime.now()
    >>>
    >>> with schedule_tweet.session(username, password) as session:
    ...     dt = now_dt + timedelta(minutes=2)
    ...     session.tweet(dt, f'First Tweet 🚀 {dt.isoformat()}')
    ...
    ...     dt = now_dt + timedelta(minutes=3)
    ...     session.tweet(dt, f'Second Tweet 💥 {dt.isoformat()}')

Multiple Accounts
-----------------

If you have multiple accounts in your TweetDeck, you can specify the account to tweet from by ``session.tweet(dt, text, username='different_account')``. By default the tweet gets sent from the initial ``username``.

Images
------

Not supported yet. Contribute! `This <https://stackoverflow.com/q/18823139/325365>`_ could help you. Note that scheduled tweets can have only one image (TweetDeck limitation).

Tests
-----

Obviously, TweetDeck authors can change anything anytime, which may or may not break this tool. That's why it is tested by a `regular nightly Travis CI build <https://travis-ci.org/honzajavorek/schedule-tweet>`_. If it's able to schedule a tweet in the sample `@schedule_tw <https://twitter.com/schedule_tw>`_ account, it assumes the tool still works and the build will pass. If the build badge is red, it means the tool doesn't work anymore and it needs to be updated.

I made the library to itch my own scratch. If it gets broken, there is some probability I'll need to use it, I'll fix it, and I'll release a new version. Otherwise I provide no support as I don't really have time to do proper maintenance of the project. I'll gladly review and accept Pull Requests though.

.. image:: https://travis-ci.org/honzajavorek/schedule-tweet.svg?branch=master
    :target: https://travis-ci.org/honzajavorek/schedule-tweet

The same tests run every time there is any change on the ``master`` branch.

Why
---

Twitter doesn't provide tweets scheduling in `their API <https://developer.twitter.com/>`_. It is provided only as a feature of `TweetDeck <http://tweetdeck.twitter.com/>`_, their advanced official client. Unlike other clients which support tweets scheduling, TweetDeck is free of charge, it is an official tool made by Twitter themselves, and it supports `teams <https://blog.twitter.com/official/en_us/a/2015/introducing-tweetdeck-teams.html>`_.

The ``schedule-tweet`` tool was originally built to save precious volunteering time of the `PyCon CZ <https://cz.pycon.org/>`_ social media team.

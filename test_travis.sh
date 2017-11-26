#!/bin/sh
set -e


pylama *.py schedule_tweet tests


if [[ $TRAVIS_PULL_REQUEST = 'false' ]]; then
    if [[ $TRAVIS_BRANCH = 'master' ]]; then
        python test_nightly.py
    else
        echo "Nightly tests run only on the 'master' branch, this is '$TRAVIS_BRANCH'";
    fi
else
    echo "Nightly tests run only on the 'master' branch, this is PR #$TRAVIS_PULL_REQUEST";
fi

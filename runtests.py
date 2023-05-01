#!/usr/bin/env python

import sys
import django
from django.conf import settings
from django.test.runner import DiscoverRunner

APP_NAME = "addressbook"

if not settings.configured:
    settings_dict = {
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        "INSTALLED_APPS": [
            "django.contrib.auth",
            "django.contrib.contenttypes",
            APP_NAME,
        ],
        "SITE_ID": 1,
        "SITE_NAME": "Test site name",
        "SECRET_KEY": "this-is-just-for-tests-so-not-that-secret",
    }
    settings.configure(**settings_dict)
    django.setup()


def runtests():
    test_runner = DiscoverRunner(verbosity=1, failfast=False)
    failures = test_runner.run_tests([APP_NAME])
    sys.exit(failures)


if __name__ == "__main__":
    runtests()

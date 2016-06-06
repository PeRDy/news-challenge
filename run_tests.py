# -*- coding: utf-8 -*-
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_challenge.settings.tests')

    if hasattr(django, "setup"):
        django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(["."])

    if failures:
        sys.exit(bool(failures))

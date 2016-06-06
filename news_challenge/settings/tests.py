# -*- coding: utf-8 -*-
"""
Unit tests in local
"""
from news_challenge.settings.development import *

# Logging
LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.NullHandler',
}

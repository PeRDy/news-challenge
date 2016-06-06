# -*- coding: utf-8 -*-
"""
Local settings.
"""
from news_challenge.settings.base import *

DEBUG = True

# Logging
LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
}
LOGGING['handlers']['news_challenge_root_file'] = {
    'level': 'DEBUG',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': '/var/log/news_challenge_root.log',
    'formatter': 'plain',
    'maxBytes': 1 * 1024 * 1024,
    'backupCount': 5,
}
LOGGING['handlers']['news_challenge_file'] = {
    'level': 'DEBUG',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': '/var/news_challenge.log',
    'formatter': 'plain',
    'maxBytes': 1 * 1024 * 1024,
    'backupCount': 5,
}

# -*- coding: utf-8 -*-
"""
Django settings.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j%5#50%kn)ns4%!uw5^vn5^i)f_+4kvz^-33z4fu4+!q6xh-b4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'material',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # REST Framework
    'rest_framework',
    # News Challenge apps
    'news_challenge',
    'news',
    # System utilities
    'gunicorn',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'news_challenge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'news_challenge.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'news_challenge',
        'HOST': 'postgres',
        'PORT': '5432',
        'USER': 'news',
        'PASSWORD': 'n3ws'
    },
}

# Cache
DEFAULT_CACHE_TIMEOUT = 60 * 15
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
            "COMPRESS_MIN_LEN": 10,
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # in seconds
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))

# Logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'json': {
            'format': '{"time":"%(asctime)s.%(msecs)dZ","level":"%(levelname)s","file":"%(name)s","line":"%(lineno)s","message":"%(message)r"}',
            'datefmt': "%Y-%m-%dT%H:%M:%S",
        },
        'plain': {
            'format': '[%(asctime)s.%(msecs)dZ] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': "%Y-%m-%dT%H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'plain'
        },
        'news_challenge_root_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/news_challenge_root.log',
            'formatter': 'json'
        },
        'news_challenge_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/news_challenge.log',
            'formatter': 'json'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'news_challenge_root_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'news_challenge': {
            'handlers': ['console', 'news_challenge_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

#########################
# Django Rest Framework
#########################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

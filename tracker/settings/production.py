from __future__ import absolute_import, unicode_literals

import os
import logging

import structlog

from .base import *  # noqa: F403, F401

try:
    from .local import *  # noqa: F403, F401
except ImportError:
    pass


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')


MIDDLEWARE += [  # noqa: F405
    'common.middleware.RequestLogMiddleware',
]


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    # Our "event_dict" is explicitly a dict
    context_class=dict,
    # Provides the logging.Logger for the underlaying log call
    logger_factory=structlog.stdlib.LoggerFactory(),
    # Provides predefined methods - log.debug(), log.info(), etc.
    wrapper_class=structlog.stdlib.BoundLogger,
    # Caching of our logger
    cache_logger_on_first_use=True,
)

pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "json_console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": pre_chain,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["json_console"], "propagate": True,
        },
        "common.views": {
            "handlers": ["json_console"], "propagate": False, "level": "DEBUG",
        },
        "request_log": {
            "handlers": ["json_console"], "propagate": False, "level": "DEBUG",
        },
        "django.template": {
            "handlers": ["json_console"], "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["json_console"], "propagate": False,
        },
        "django.security": {
            "handlers": ["json_console"], "propagate": False,
        },
        # These are already handled by the django json logging library
        "django.request": {
            "handlers": ["null"],
            "propagate": False,
        },
        # Log entries from runserver
        "django.server": {
            "handlers": ["null"], "propagate": False,
        },
        # Catchall
        "": {
            "handlers": ["json_console"], "propagate": False,
        },
    },
}


# Domain specific
#
BASE_URL = os.environ.get('DJANGO_BASE_URL', 'https://pressfreedomtracker.us')
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
MEDIA_URL = os.environ.get('DJANGO_MEDIA_URL', '/media/')

# Database settings
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DJANGO_DB_NAME'],
        'USER': os.environ['DJANGO_DB_USER'],
        'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
        'HOST': os.environ['DJANGO_DB_HOST'],
        'PORT': os.environ['DJANGO_DB_PORT'],
        'CONN_MAX_AGE': os.environ.get('DJANGO_DB_MAX_AGE', 600)
    }
}

# Static and media files
#
if os.environ.get('GS_BUCKET_NAME'):
    INSTALLED_APPS.append('storages')  # noqa: F405

    GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']

    if 'GS_CUSTOM_ENDPOINT' in os.environ:
        GS_CUSTOM_ENDPOINT = os.environ['GS_CUSTOM_ENDPOINT']

    if 'GS_CREDENTIALS' in os.environ:
        from google.oauth2.service_account import Credentials
        GS_CREDENTIALS = Credentials.from_service_account_file(os.environ['GS_CREDENTIALS'])
    elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        logging.warning('Defaulting to global GOOGLE_APPLICATION_CREDENTIALS')
    else:
        logging.warning(
            'GS_CREDENTIALS or GOOGLE_APPLICATION_CREDENTIALS unset! ' +
            'Falling back to credentials of the machine we are running on, ' +
            'if it is a GCE instance. This is almost certainly not desired.'
        )

    GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')
    GS_MEDIA_PATH = os.environ.get('GS_MEDIA_PATH', 'media')
    GS_STATIC_PATH = os.environ.get('GS_STATIC_PATH', 'static')
    GS_FILE_OVERWRITE = os.environ.get('GS_FILE_OVERWRITE') == 'True'

    DEFAULT_FILE_STORAGE = 'common.storage.MediaStorage'

    # Only whitenoise currently works. In the future, we might choose to
    # upload static files to a bucket on build instead.
    if 'GS_STORE_STATIC' in os.environ:
        STATICFILES_STORAGE = 'common.storage.StaticStorage'
else:
    if 'DJANGO_WHITENOISE' not in os.environ:
        STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')
    MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT')

# Cloudflare caching
#
if os.environ.get('CLOUDFLARE_TOKEN') and os.environ.get('CLOUDFLARE_EMAIL'):
    INSTALLED_APPS.append('wagtail.contrib.frontend_cache')  # noqa: F405
    WAGTAILFRONTENDCACHE = {
        'cloudflare': {
            'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
            'EMAIL': os.environ.get('CLOUDFLARE_EMAIL'),
            'TOKEN': os.environ.get('CLOUDFLARE_TOKEN'),
            'ZONEID': os.environ.get('CLOUDFLARE_ZONEID')
        },
    }

ANALYTICS_ENABLED = True

# Mailgun integration
#
if os.environ.get('MAILGUN_API_KEY'):
    INSTALLED_APPS.append('anymail')  # noqa: F405
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    ANYMAIL = {
        'MAILGUN_API_KEY': os.environ['MAILGUN_API_KEY'],
        'MAILGUN_SENDER_DOMAIN': os.environ['MAILGUN_SENDER_DOMAIN'],
    }
    DEFAULT_FROM_EMAIL = os.environ.get('MAILGUN_FROM_ADDR',
                                        'webmaster@mg.pressfreedomtracker.us')

# Ensure Django knows its being served over https
SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https')

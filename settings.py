# -*- coding: utf-8 -*-
import os

from django.contrib.messages import constants as messages
import djcelery

_project_root = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(_project_root, 'db.sql'),
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', u'English'),
    ('ru', u'Русский'),
)

LOCALE_PATHS = (
    os.path.join(_project_root, 'locale'),
)

DATE_INPUT_FORMATS = ['%d.%m.%Y']

SITE_ID = 1
USE_I18N = True
USE_L10N = False

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(_project_root, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'personal.middleware.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djcelery',
    'south',
    'personal',
    'picasa',
    'management',
    'frontend',
)

AUTH_PROFILE_MODULE = 'personal.UserProfile'
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

PHOTO_SIZE = 900

PICASA_SCOPES = (
    'http://picasaweb.google.com/data/feed/',
    'https://picasaweb.google.com/data/feed/',
)

FORCE_SCRIPT_NAME = '' # Workaround for lighttpd webserver

GOOGLE_TOKEN_MANAGEMENT_URL = 'https://accounts.google.com/b/0/IssuedAuthSubTokens'

MESSAGE_TAGS = {
    messages.INFO: 'alert-info',
    messages.ERROR: 'alert-error',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: '',
}

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_IMPORTS = (
    'picasa.async',
)

from secret_settings import *
# SECRET_KEY
# ADMINS

# PICASA_RSA_KEY

# BROKER_HOST
# BROKER_BACKEND
# REDIS_PORT
# REDIS_HOST
# BROKER_USER
# BROKER_PASSWORD
# BROKER_VHOST
# REDIS_DB
# REDIS_CONNECT_RETRY
# CELERY_SEND_EVENTS
# CELERY_RESULT_BACKEND
# CELERY_TASK_RESULT_EXPIRES

djcelery.setup_loader()

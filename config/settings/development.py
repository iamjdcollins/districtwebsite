from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'schools-dev.slcschools.org',
    'www-dev.slcschools.org',
    'horizonte-dev.slcschools.org',
]

# Required for Django Debug Toolbar
INTERNAL_IPS = '127.0.0.1'

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}
from .base import *

DEBUG = True

# Required for Django Debug Toolbar
INTERNAL_IPS='127.0.0.1'

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

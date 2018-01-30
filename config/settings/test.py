from .base import *

ALLOWED_HOSTS = ['www-test.slcschools.org',]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp'

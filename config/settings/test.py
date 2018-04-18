from .base import *

ALLOWED_HOSTS = [
    'websites-test.slcschools.org',
    'www-test.slcschools.org',
    'horizonte-test.slcschools.org',
]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp'

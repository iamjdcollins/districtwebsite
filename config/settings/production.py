from .base import *

ALLOWED_HOSTS = ['www.slcschools.org','www2.slcschools.org',]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'slcschools-org.mail.protection.outlook.com'
EMAIL_PORT = '25'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 25


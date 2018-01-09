from .base import *

SAML2_AUTH['ASSERTION_URL'] = 'https://www2.slcschools.org'

ALLOWED_HOSTS = ['www.slcschools.org','www2.slcschools.org',]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True


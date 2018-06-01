from .base import *

ENVIRONMENT_MODE = 'production'

ALLOWED_HOSTS = [
    'backman.slcschools.org',
    'beaconheights.slcschools.org',
    'bennion.slcschools.org',
    'bonneville.slcschools.org',
    'bryant.slcschools.org',
    'clayton.slcschools.org',
    'dilworth.slcschools.org',
    'east.slcschools.org',
    'edison.slcschools.org',
    'emerson.slcschools.org',
    'ensign.slcschools.org',
    'escalante.slcschools.org',
    'franklin.slcschools.org',
    'glendale.slcschools.org',
    'hawthorne.slcschools.org',
    'highland.slcschools.org',
    'highlandpark.slcschools.org',
    'hillside.slcschools.org',
    'horizonte.slcschools.org',
    'horizonte.slcschools.org',
    'indianhills.slcschools.org',
    'innovations.slcschools.org',
    'innovations.slcschools.org',
    'liberty.slcschools.org',
    'maryjackson.slcschools.org',
    'meadowlark.slcschools.org',
    'mountainview.slcschools.org',
    'newman.slcschools.org',
    'nibleypark.slcschools.org',
    'northstar.slcschools.org',
    'northwest.slcschools.org',
    'parkview.slcschools.org',
    'riley.slcschools.org',
    'rosepark.slcschools.org',
    'uintah.slcschools.org',
    'wasatch.slcschools.org',
    'washington.slcschools.org',
    'websites.slcschools.org',
    'west.slcschools.org',
    'whittier.slcschools.org',
    'www.ocslc.org',
    'www.saltlakespa.org',
    'www.slcschools.org',
    'www.slcse.org',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'slcschools-org.mail.protection.outlook.com'
EMAIL_PORT = '25'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 25


STATIC_URL = 'https://websites.slcschools.org/static/'

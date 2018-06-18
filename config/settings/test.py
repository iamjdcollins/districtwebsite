from .base import *

ENVIRONMENT_MODE = 'test'

ALLOWED_HOSTS += [
    'backman-test.slcschools.org',
    'beaconheights-test.slcschools.org',
    'bennion-test.slcschools.org',
    'bonneville-test.slcschools.org',
    'bryant-test.slcschools.org',
    'clayton-test.slcschools.org',
    'dilworth-test.slcschools.org',
    'east-test.slcschools.org',
    'edison-test.slcschools.org',
    'emerson-test.slcschools.org',
    'ensign-test.slcschools.org',
    'escalante-test.slcschools.org',
    'franklin-test.slcschools.org',
    'glendale-test.slcschools.org',
    'hawthorne-test.slcschools.org',
    'highland-test.slcschools.org',
    'highlandpark-test.slcschools.org',
    'hillside-test.slcschools.org',
    'horizonte-test.slcschools.org',
    'horizonte-test.slcschools.org',
    'indianhills-test.slcschools.org',
    'innovations-test.slcschools.org',
    'innovations-test.slcschools.org',
    'liberty-test.slcschools.org',
    'maryjackson-test.slcschools.org',
    'meadowlark-test.slcschools.org',
    'mountainview-test.slcschools.org',
    'newman-test.slcschools.org',
    'nibleypark-test.slcschools.org',
    'northstar-test.slcschools.org',
    'northwest-test.slcschools.org',
    'parkview-test.slcschools.org',
    'riley-test.slcschools.org',
    'rosepark-test.slcschools.org',
    'uintah-test.slcschools.org',
    'wasatch-test.slcschools.org',
    'washington-test.slcschools.org',
    'websites-test.slcschools.org',
    'west-test.slcschools.org',
    'whittier-test.slcschools.org',
    'www-test.ocslc.org',
    'www-test.saltlakespa.org',
    'www-test.slcschools.org',
    'www-test.slcse.org',
]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp'

STATIC_URL = 'https://websites-test.slcschools.org/static/'

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'backman-dev.slcschools.org',
    'beaconheights-dev.slcschools.org',
    'bennion-dev.slcschools.org',
    'bonneville-dev.slcschools.org',
    'bryant-dev.slcschools.org',
    'clayton-dev.slcschools.org',
    'dilworth-dev.slcschools.org',
    'east-dev.slcschools.org',
    'edison-dev.slcschools.org',
    'emerson-dev.slcschools.org',
    'ensign-dev.slcschools.org',
    'escalante-dev.slcschools.org',
    'franklin-dev.slcschools.org',
    'glendale-dev.slcschools.org',
    'hawthorne-dev.slcschools.org',
    'highland-dev.slcschools.org',
    'highlandpark-dev.slcschools.org',
    'hillside-dev.slcschools.org',
    'horizonte-dev.slcschools.org',
    'horizonte-dev.slcschools.org',
    'indianhills-dev.slcschools.org',
    'innovations-dev.slcschools.org',
    'innovations-dev.slcschools.org',
    'liberty-dev.slcschools.org',
    'maryjackson-dev.slcschools.org',
    'meadowlark-dev.slcschools.org',
    'mountainview-dev.slcschools.org',
    'newman-dev.slcschools.org',
    'nibleypark-dev.slcschools.org',
    'northstar-dev.slcschools.org',
    'northwest-dev.slcschools.org',
    'parkview-dev.slcschools.org',
    'riley-dev.slcschools.org',
    'rosepark-dev.slcschools.org',
    'uintah-dev.slcschools.org',
    'wasatch-dev.slcschools.org',
    'washington-dev.slcschools.org',
    'websites-dev.slcschools.org',
    'west-dev.slcschools.org',
    'whittier-dev.slcschools.org',
    'www-dev.ocslc.org',
    'www-dev.saltlakespa.org',
    'www-dev.slcschools.org',
    'www-dev.slcse.org',
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

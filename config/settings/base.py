"""
Django settings for www_slcschools_org project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['WWW_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#SAML
SAML2_AUTH = {
    'METADATA_AUTO_CONF_URL': 'https://adfs.slcschools.org/FederationMetadata/2007-06/FederationMetadata.xml',
    'ATTRIBUTES_MAP': {  # Change Email/UserName/FirstName/LastName to corresponding SAML2 userprofile attributes.
        'email': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
        'username': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn',
        'first_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname',
        'last_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
    },
}

AUTH_USER_MODEL = 'objects.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

# Application definition

INSTALLED_APPS = [
    #'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'apps.thirdparty.django_saml2_auth',
    'guardian',
    'mptt',
    'ckeditor',
    'ajax_select',
    'adminsortable2',
    'www_slcschools_org',
    'apps.objects',
    'apps.taxonomy',
    'apps.users',
    'apps.pages',
    'apps.images',
    'apps.directoryentries',
    'apps.links',
    'apps.files',
    'apps.documents',
    'apps.events',
    'apps.faqs',
    'apps.contact_messages',
    #'apps.schools',
    #'apps.board',
    #'apps.news',
    #'apps.departments'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.common.processors.currentyear',
                'apps.taxonomy.processors.translationlinks',
                'apps.objects.processors.breadcrumb',
                'apps.objects.processors.mainmenu',
                'apps.objects.processors.sitestructure',
            ],
            'loaders': [
                 ('django.template.loaders.cached.Loader', [
                     'django.template.loaders.filesystem.Loader',
                     'django.template.loaders.app_directories.Loader',
                 ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': os.environ['WWW_DB_NAME'],
      'USER': os.environ['WWW_DB_USER'],
      'PASSWORD': os.environ['WWW_DB_PASSWORD'],
      'HOST': os.environ['WWW_DB_HOST'],
      'PORT': os.environ['WWW_DB_PORT'],
      'CONN_MAX_AGE': 600,
      'OPTIONS': {
          'connect_timeout': 0
      },
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
DATA_DIR = '/srv/nginx/www_slcschools_org'
MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(DATA_DIR)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/var/run/memcached/memcached.sock',
    }
}

SLCSD_LDAP_USER = os.environ['SLCSD_LDAP_USER']
SLCSD_LDAP_PASSWORD = os.environ['SLCSD_LDAP_PASSWORD']


#DEFAULT_CONFIG = {
#    'skin': 'moono-lisa',
#    'toolbar_Basic': [
#        ['Source', '-', 'Bold', 'Italic']
#    ],
#    'toolbar_Full': [
#        ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
#        ['Link', 'Unlink', 'Anchor'],
#        ['Image', 'Flash', 'Table', 'HorizontalRule'],
#        ['TextColor', 'BGColor'],
#        ['Smiley', 'SpecialChar'], ['Source'],
#    ],
#    'toolbar': 'Full',
#    'height': 291,
#    'width': 835,
#    'filebrowserWindowWidth': 940,
#    'filebrowserWindowHeight': 725,
#}


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'SLCSD',
        'toolbar_SLCSD': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Undo', 'Redo'],
            ['NumberedList', 'BulletedList'],
            #['Link', 'Unlink'],
            ['Table', 'HorizontalRule'],
            #['Source']
            ['Departments',],
        ],
        'format_tags': 'p;h3;h4;h5;h6',
        'autoGrow_bottomSpace': 10,
        'autoGrow_maxHeight': 0,
        'autoGrow_onStartup': True,
        'extraPlugins': ','.join([
            'autogrow','departments',
        ]),
        'disableNativeSpellChecker': False,
        #'allowedContent': 'p h3 h4 h5 h6 strong em u s ol ul li table caption thead tbody tr th td hr br',
        'extraAllowedContent': 'a(!relink)[!data-id]',
    }
}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/www_slcschools_org',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores',
    },
}

"""
Django settings for www_slcschools_org project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from multisite import SiteID

# Django Multisite SiteID
SITE_ID = SiteID(default=1)

ADMINS = [
    ('Jordan Collins', 'jordan.collins@slcschools.org'),
]


def localaddresses():
  import netifaces
  ifaces = netifaces.interfaces()
  addrs = []
  for iface in netifaces.interfaces():
    for addr in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
      addrs.append(addr['addr'])
  return addrs


LOCAL_ADDRESSES = localaddresses()

ALLOWED_HOSTS = [] + LOCAL_ADDRESSES

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# Load Secrets
def load_secrets(file=os.path.join(BASE_DIR, '.secrets.json')):
    try:
        with open(file) as f:
            secrets = json.loads(f.read())
            return secrets
    except FileNotFoundError:
        raise ImproperlyConfigured(
            'Secrets file not found. Please create the secrets file or correct'
            ' the configuration.'
        )


secrets = load_secrets()


# Get a secret
def get_secret(key, secrets=secrets or load_secrets()):
    try:
        val = secrets[key]
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        return val
    except KeyError:
        error_msg = (
            "ImproperlyConfigured: Set {0} environment variable"
        ).format(key)
        raise ImproperlyConfigured(error_msg)

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o775
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_TEMP_DIR='/srv/nginx/tmp/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SAML
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
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

# Application definition
INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'multisite',
    'haystack',
    'apps.thirdparty.django_saml2_auth.django_saml2_auth',
    'guardian',
    'mptt',
    'pipeline',
    'ckeditor',
    'ajax_select',
    'adminsortable2',
    'imagekit',
    'apps.cmstemplates',
    'apps.dashboard',
    'apps.medialibrary',
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
    'apps.contactmessages',
]

CACHE_MIDDLEWARE_SECONDS = 0

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'multisite.middleware.DynamicSiteMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    # 'apps.common.middleware.DynamicDataDir',
    'django.middleware.cache.FetchFromCacheMiddleware',
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
                'apps.common.processors.environmentmode',
                'apps.taxonomy.processors.translationlinks',
                'apps.objects.processors.breadcrumb',
                'apps.objects.processors.mainmenu',
                'apps.objects.processors.sitestructure',
                'apps.objects.processors.is_siteadmin',
                'apps.objects.processors.is_globaladmin',
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

DATA_UPLOAD_MAX_MEMORY_SIZE = None
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': get_secret('DEFAULT_DATABASE_ENGINE'),
        'NAME': get_secret('DEFAULT_DATABASE_NAME'),
        'USER': get_secret('DEFAULT_DATABASE_USER'),
        'PASSWORD': get_secret('DEFAULT_DATABASE_PASSWORD'),
        'HOST': get_secret('DEFAULT_DATABASE_HOST'),
        'PORT': get_secret('DEFAULT_DATABASE_PORT'),
        'CONN_MAX_AGE': 20,
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
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/var/run/memcached/memcached.sock',
    },
}

DATA_DIR = '/srv/nginx/websites.slcschools.org'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

SLCSD_LDAP_USER = get_secret('SLCSD_LDAP_USER')
SLCSD_LDAP_PASSWORD = get_secret('SLCSD_LDAP_PASSWORD')


# DEFAULT_CONFIG = {
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
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList'],
            ['Relink', 'Imagewidget', 'Iframe'],
            ['Table', 'HorizontalRule'],
        ],
        'format_tags': 'p;h3;h4;h5;h6',
        'autoGrow_bottomSpace': 10,
        'autoGrow_maxHeight': 0,
        'autoGrow_onStartup': True,
        'removePlugins': 'link, unlink, image, image2',
        'extraPlugins': ','.join([
            'autogrow', 'relink', 'fixed', 'uploadimage', 'imagewidget',
        ]),
        'disableNativeSpellChecker': False,
        'image2_altRequired': True,
        'image2_disableResizer': True,
        'uploadUrl': '/',
        'filebrowserImagewidgetBrowseUrl': '/medialibrary/',
        'filebrowserWindowFeatures': 'location=no,menubar=no,toolbar=no,dependent=yes,minimizable=no,modal=yes,alwaysRaised=yes,resizable=no,scrollbars=yes',
        # 'filebrowserUploadUrl': '/test/',
        # 'allowedContent': 'p h3 h4 h5 h6 strong em u s ol ul li table caption thead tbody tr th td hr br',
        # 'extraAllowedContent': 'a(!relink)[!data-id]',
    },
}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/www_slcschools_org',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores',
    },
}

CACHE_MULTISITE_ALIAS = 'default'
CACHE_MULTISITE_KEY_PREFIX = 'multisite'
MULTISITE_FALLBACK = 'apps.common.functions.multisite_fallback_view'


class ImagekitCacheFileSystemStorage(FileSystemStorage):
  location = DATA_DIR
  base_url = '/'
  file_permissions_mode = 0o664
  directory_permissions_mode = 0o775


# Image Kit Settings
IMAGEKIT_DEFAULT_FILE_STORAGE = (
    'config.settings.base.ImagekitCacheFileSystemStorage'
)
# IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.hash'
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'apps.common.functions.name_dot_field_dot_ext'
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'apps.common.classes.Simple'
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'apps.common.classes.JustInTime'
IMAGEKIT_CACHEFILE_DIR = 'cache'

# CMSTEMPLATES

CMSTEMPLATES = {
    'css': {
        'frameworks': {
            'materialize': [
                'cmstemplates/src/frameworks/materialize/sass/materialize.scss',
            ],
            'purecss': [
                'cmstemplates/src/frameworks/purecss/pure-min.css',
            ],
        },
        'fonts': {
            'md': [
                'cmstemplates/src/fonts/md/md.css',
            ],
        },
        'templates': {
            'global': [
                'cmstemplates/src/templates/global/sass/global.scss',
            ],
            'backend': [
                'cmstemplates/src/templates/backend/sass/backend.scss',
            ],
            'frontend': [
                'cmstemplates/src/templates/frontend/sass/frontend.scss',
            ],
            'dashboard': [
                'cmstemplates/src/templates/dashboard/sass/dashboard.scss',
            ],
            'material': [
                'cmstemplates/src/templates/material/sass/material.scss',
            ],
            'innovate': [
                'cmstemplates/src/templates/innovate/sass/innovate.scss',
            ],
            'inspire': [
                'cmstemplates/src/templates/inspire/sass/inspire.scss',
            ],
        },
        'themes': {
            'dashboard-standard': [
                'cmstemplates/src/themes/dashboard-standard/sass/dashboard-standard.scss',
            ],
            'material-standard': [
                'cmstemplates/src/themes/material-standard/sass/material-standard.scss',
            ],
            'innovate-standard': [
                'cmstemplates/src/themes/innovate-standard/sass/innovate-standard.scss',
            ],
            'inspire-standard': [
                'cmstemplates/src/themes/inspire-standard/sass/inspire-standard.scss',
            ],
        },
        'modaal043': [
            'cmstemplates/src/modaal043/css/modaal.min.css',
        ],
    },
    'javascript': {
        'jquery211': [
            'cmstemplates/src/js/jquery/jquery.2.1.1.js',
        ],
        'modaal043': [
            'cmstemplates/src/modaal043/js/modaal.min.js',
        ],

        'materialize': [
            'cmstemplates/src/frameworks/materialize/js/bin/materialize.js',
        ],
        'global': [
            'cmstemplates/src/js/templates/global/global.js',
        ],
        'backend': [
            'cmstemplates/src/js/templates/backend/backend.js',
        ],
        'frontend': [
            'cmstemplates/src/js/templates/frontend/frontend.js',
        ],
        'dashboard': [
            'cmstemplates/src/js/templates/dashboard/dashboard.js',
        ],
        'material': [
            'cmstemplates/src/js/templates/material/material.js',
        ],
        'innovate': [
            'cmstemplates/src/js/templates/innovate/innovate.js',
        ],
        'inspire': [
            'cmstemplates/src/js/templates/inspire/inspire.js',
        ],
    },
}

# Django Pipeline

PIPELINE = {
    'COMPILERS': (
        'libsasscompiler.LibSassCompiler',
    ),
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'STYLESHEETS': {
        'dashboard-standard': {
            'source_filenames': CMSTEMPLATES['css']['frameworks']['materialize'] + CMSTEMPLATES['css']['fonts']['md'] + CMSTEMPLATES['css']['templates']['global'] + CMSTEMPLATES['css']['templates']['backend'] + CMSTEMPLATES['css']['templates']['dashboard'] + CMSTEMPLATES['css']['themes']['dashboard-standard'],
            'output_filename': 'cmstemplates/build/dashboard-standard/dashboard-standard.min.css',
        },
        'medialibrary': {
            'source_filenames': CMSTEMPLATES['css']['frameworks']['purecss'] + CMSTEMPLATES['css']['fonts']['md'],
            'output_filename': 'cmstemplates/build/medialibrary/medialibrary.min.css',
        },
        'material-standard': {
            'source_filenames': CMSTEMPLATES['css']['frameworks']['purecss'] + CMSTEMPLATES['css']['fonts']['md'] + CMSTEMPLATES['css']['modaal043'] + CMSTEMPLATES['css']['templates']['global'] + CMSTEMPLATES['css']['templates']['frontend'] + CMSTEMPLATES['css']['templates']['material'] + CMSTEMPLATES['css']['themes']['material-standard'],
            'output_filename': 'cmstemplates/build/material-standard/material-standard.min.css',
        },
        'innovate-standard': {
            'source_filenames': CMSTEMPLATES['css']['frameworks']['purecss'] + CMSTEMPLATES['css']['fonts']['md'] + CMSTEMPLATES['css']['modaal043'] + CMSTEMPLATES['css']['templates']['global'] + CMSTEMPLATES['css']['templates']['frontend'] + CMSTEMPLATES['css']['templates']['innovate'] + CMSTEMPLATES['css']['themes']['innovate-standard'],
            'output_filename': 'cmstemplates/build/innovate-standard/innovate-standard.min.css',
        },
        'inspire-standard': {
            'source_filenames': CMSTEMPLATES['css']['frameworks']['purecss'] + CMSTEMPLATES['css']['fonts']['md'] + CMSTEMPLATES['css']['modaal043'] + CMSTEMPLATES['css']['templates']['global'] + CMSTEMPLATES['css']['templates']['frontend'] + CMSTEMPLATES['css']['templates']['inspire'] + CMSTEMPLATES['css']['themes']['inspire-standard'],
            'output_filename': 'cmstemplates/build/inspire-standard/inspire-standard.min.css',
        },
        'horizonte': {
            'source_filenames': ['cmstemplates/src/themes/horizonte/sass/horizonte.scss'],
            'output_filename': 'cmstemplates/build/horizonte/horizonte.min.css',
        },
        'innovations': {
            'source_filenames': ['cmstemplates/src/themes/innovations/sass/innovations.scss'],
            'output_filename': 'cmstemplates/build/innovations/innovations.min.css',
        },
    },
    'JAVASCRIPT': {
        'dashboard-standard': {
            'source_filenames': CMSTEMPLATES['javascript']['jquery211'] + CMSTEMPLATES['javascript']['materialize'] + CMSTEMPLATES['javascript']['global'] + CMSTEMPLATES['javascript']['backend'] + CMSTEMPLATES['javascript']['dashboard'],
            'output_filename': 'cmstemplates/build/dashboard-standard/dashboard-standard.min.js',
        },
        'material-standard': {
            'source_filenames': CMSTEMPLATES['javascript']['jquery211'] + CMSTEMPLATES['javascript']['modaal043'] + CMSTEMPLATES['javascript']['global'] + CMSTEMPLATES['javascript']['frontend'] + CMSTEMPLATES['javascript']['material'],
            'output_filename': 'cmstemplates/build/material-standard/material-standard.min.js',
        },
        'innovate-standard': {
            'source_filenames': CMSTEMPLATES['javascript']['jquery211'] + CMSTEMPLATES['javascript']['modaal043'] + CMSTEMPLATES['javascript']['global'] + CMSTEMPLATES['javascript']['frontend'] + CMSTEMPLATES['javascript']['innovate'],
            'output_filename': 'cmstemplates/build/innovate-standard/innovate-standard.min.js',
        },
        'inspire-standard': {
            'source_filenames': CMSTEMPLATES['javascript']['jquery211'] + CMSTEMPLATES['javascript']['modaal043'] + CMSTEMPLATES['javascript']['global'] + CMSTEMPLATES['javascript']['frontend'] + CMSTEMPLATES['javascript']['inspire'],
            'output_filename': 'cmstemplates/build/inspire-standard/inspire-standard.min.js',
        },
    },
}

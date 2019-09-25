"""
Django settings for student_explorer project.

By default the application does not use this module, it reads settings from
student_explorer.local.settings, create that module and add
    from student_explorer.settings import *
to the top, then override settings initialized in this module.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, json
from decouple import config, Csv

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default='off', cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', 'localhost', cast=Csv())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='I need to be changed!')

SESSION_COOKIE_AGE = config('DJANGO_SESSION_COOKIE_AGE', default=36000, cast=int)
SESSION_SAVE_EVERY_REQUEST = config('DJANGO_SESSION_SAVE_EVERY_REQUEST', default='on', cast=bool)

SILENCED_SYSTEM_CHECKS = []

ADMINS = [('', config('DJANGO_ERROR_EMAIL', default='vagrant@localhost'))]


# Application definition

INSTALLED_APPS = (
    'cachalot',
    'django_ptvsd',
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cron',
    'watchman',
    'student_explorer',
    'seumich',
    'management',
    'tracking',
    'feedback',
    'usage',
)

CRON_CLASSES = [
    "student_explorer.cron.StudentExplorerCronJob",
]

# Time to run cron
RUN_AT_TIMES = config('RUN_AT_TIMES', default="", cast= Csv())

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'student_explorer.middleware.LoggingMiddleware',
    'student_explorer.middleware.HttpResourceNotAllowedMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'student_explorer.context_processors.last_updated',
            ],
        },
    },
]

ROOT_URLCONF = 'student_explorer.urls'

WSGI_APPLICATION = 'student_explorer.wsgi.application'

USE_X_FORWARDED_HOST = config('DJANGO_USE_X_FORWARDED_HOST', default='no', cast=bool)

FORCE_SCRIPT_NAME = config('DJANGO_FORCE_SCRIPT_NAME', default=None)

WATCHMAN_TOKEN = config('DJANGO_WATCHMAN_TOKEN', default=None)
WATCHMAN_TOKEN_NAME = config('DJANGO_WATCHMAN_TOKEN_NAME', default='token')

DOWNLOAD_TOKEN = config('DJANGO_DOWNLOAD_TOKEN', default=None)

PAGINATION_RECORDS_PER_PAGE = config('DJANGO_PAGINATION_RECORDS_PER_PAGE', default=10, cast=int)
PAGINATION_NUM_PAGE_LINKS = config('DJANGO_PAGINATION_NUM_PAGE_LINKS', default=5, cast=int)

SERVER_EMAIL = config('DJANGO_SERVER_EMAIL',
                      default='student-explorer-admins@umich.edu')

USAGE_PAST_WEEKS = config('DJANGO_USAGE_PAST_WEEKS', default=8, cast=int)

# Internationalization

LANGUAGE_CODE = config('DJANGO_LANGUAGE_CODE', default='en-us')

TIME_ZONE = config('DJANGO_TIME_ZONE', default='America/Detroit')

USE_I18N = config('DJANGO_USE_I18N', default='yes', cast=bool)

USE_L10N = config('DJANGO_USE_L10N', default='yes', cast=bool)

USE_TZ = config('DJANGO_USE_TZ', default='yes', cast=bool)


# Static files (CSS, JavaScript, Images)

STATIC_URL = config('DJANGO_STATIC_URL', default='/static/')
STATIC_ROOT = config('DJANGO_STATIC_ROOT',
                     default=os.path.join(BASE_DIR, 'staticfiles'))

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = config('DJANGO_LOGIN_URL', default='/accounts/login/')
LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = config('DJANGO_LOGOUT_REDIRECT_URL', default='/')

EMAIL_HOST = config('DJANGO_EMAIL_HOST', default='localhost')
EMAIL_PORT = config('DJANGO_EMAIL_PORT', default=25)
EMAIL_HOST_USER = config('DJANGO_EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('DJANGO_EMAIL_HOST_PASSWORD', default=None)
EMAIL_USE_TLS = config('DJANGO_EMAIL_USE_TLS', default=None)
EMAIL_USE_SSL = config('DJANGO_EMAIL_USE_SSL', default=None)

FEEDBACK_EMAIL = config('DJANGO_FEEDBACK_EMAIL', default=None)

# Databases

DATABASES = {}
DATABASE_ROUTERS = []

DATABASES['default'] = {
    'ENGINE': config('DJANGO_DB_ENGINE', default='django.db.backends.mysql'),
    'NAME': config('DJANGO_DB_NAME', default='student_explorer'),
    'USER': config('DJANGO_DB_USER', default='student_explorer'),
    'PASSWORD': config('DJANGO_DB_PASSWORD', default='student_explorer'),
    'HOST': config('DJANGO_DB_HOST', default=''),
    'PORT': config('DJANGO_DB_PORT', default=''),
}

DATABASES['seumich'] = {
    'ENGINE': config('DJANGO_SEUMICH_DB_ENGINE', default='django.db.backends.mysql'),
    'NAME': config('DJANGO_SEUMICH_DB_NAME', default='student_explorer'),
    'USER': config('DJANGO_SEUMICH_DB_USER', default='student_explorer'),
    'PASSWORD': config('DJANGO_SEUMICH_DB_PASSWORD', default='student_explorer'),
    'HOST': config('DJANGO_SEUMICH_DB_HOST', default=''),
    'PORT': config('DJANGO_SEUMICH_DB_PORT', default=''),
    'MIGRATE': config('DJANGO_SEUMICH_DB_MIGRATE', default='no', cast=bool),

}
DATABASE_ROUTERS += ['seumich.routers.SeumichRouter']


# SAML Auth

if config('STUDENT_EXPLORER_SAML', default='no', cast=bool):
    SAML2_URL_PATH = config('STUDENT_EXPLORER_SAML_URL_PATH', default='/accounts/')
    SAML2_URL_BASE = config('STUDENT_EXPLORER_SAML_URL_BASE',
                            default='http://localhost:2082/accounts/')

    SAML2_REMOTE_METADATA = config('STUDENT_EXPLORER_SAML_REMOTE_METADATA',default='')
    SAML2_REMOTE_PEM_FILE = config('STUDENT_EXPLORER_SAML_REMOTE_PEM_FILE',default='')

    SAML2_DEFAULT_IDP = config('STUDENT_EXPLORER_SAML_DEFAULT_IDP',default='')

    if SAML2_DEFAULT_IDP:
        SAML2_DEFAULT_IDP = '?idp=%s' % SAML2_DEFAULT_IDP

    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        # Use a custom SAML backend to support disabled users
        'student_explorer.backends.ActiveUserOnlySAML2Backend',
    )
    LOGIN_URL = '%slogin/%s' % (SAML2_URL_PATH, SAML2_DEFAULT_IDP)
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    import saml2
    SAML_CONFIG = {
      'xmlsec_binary': '/usr/bin/xmlsec1',
      'entityid': '%smetadata/' % SAML2_URL_BASE,

      # directory with attribute mapping
      # 'attribute_map_dir': os.path.join(BASE_DIR, 'attribute-maps'),
      'name': config('STUDENT_EXPLORER_SAML_SERVICE_NAME', default='Student Explorer'),
      # this block states what services we provide
      'service': {
          # we are just a lonely SP
          'sp': {
              'name': 'Student Explorer',
              'name_id_format': config(
                'STUDENT_EXPLORER_SAML_NAME_ID_FORMAT',
                default='urn:oasis:names:tc:SAML:2.0:nameid-format:transient'),
              'authn_requests_signed': 'true',
              'allow_unsolicited': True,
              'endpoints': {
                  # url and binding to the assetion consumer service view
                  # do not change the binding or service name
                  'assertion_consumer_service': [
                      ('%sacs/' % SAML2_URL_BASE,
                       saml2.BINDING_HTTP_POST),
                      ],
                  # url and binding to the single logout service view
                  # do not change the binding or service name
                  'single_logout_service': [
                      ('%sls/' % SAML2_URL_BASE,
                       saml2.BINDING_HTTP_REDIRECT),
                      ('%sls/post' % SAML2_URL_BASE,
                       saml2.BINDING_HTTP_POST),
                      ],
                  },

              # attributes that this project need to identify a user
              'required_attributes': ['uid'],

              # attributes that may be useful to have but not required
              'optional_attributes': ['eduPersonAffiliation'],
              },
          },

      'metadata': [{
          "class": "saml2.mdstore.MetaDataExtern",
          "metadata": [
              (SAML2_REMOTE_METADATA, SAML2_REMOTE_PEM_FILE)]
      }],

      # set to 1 to output debugging information
      'debug': DEBUG,

      # certificate
      'key_file': os.path.join(
        BASE_DIR, 'student_explorer/local/saml/student-explorer-saml.key'),
      'cert_file': os.path.join(
        BASE_DIR, 'student_explorer/local/saml/student-explorer-saml.pem'),
      }

SAML_CREATE_UNKNOWN_USER = False

SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username', ),
    'mail': ('email', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'all': {
            'format': ('%(levelname)s %(asctime)s %(module)s %(process)d '
                       '%(thread)d %(message)s'),
        },
        'debug': {
            'format': ('%(asctime)s %(levelname)s %(message)s '
                       '%(pathname)s:%(lineno)d'),
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
        'access_logs': {
            'format': ('%(message)s'),
        },

    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': config('DJANGO_LOGGING_LEVEL_EMAIL_ADMINS', default='ERROR'),
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'access_logs': {
            'class': 'logging.StreamHandler',
            'formatter': 'access_logs',
        },
    },
    'loggers': {
        '': {
            'handlers': ['mail_admins'],
            'level': config('DJANGO_LOGGING_LEVEL_EMAIL_ADMINS', default='ERROR'),
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOGGING_LEVEL', default='WARNING'),
        },
        'se_umich': {
            'handlers': ['console'],
            'level': config('DJANGO_LOGGING_LEVEL', default='WARNING'),
        },
        'feedback': {
            'handlers': ['console'],
            'level': config('DJANGO_LOGGING_LEVEL', default='WARNING'),
        },
        'tracking': {
            'handlers': ['console'],
            'level': config('DJANGO_LOGGING_LEVEL', default='WARNING'),
        },
        'student_explorer': {
            'handlers': ['console'],
            'level': config('DJANGO_LOGGING_LEVEL', default='WARNING'),
        },
        'access_logs': {
            'handlers': ['access_logs'],
            'level': 'INFO',
        },
    },
}

# Defaults for PTVSD
PTVSD_ENABLE = config("PTVSD_ENABLE", default=False, cast=bool)
PTVSD_REMOTE_ADDRESS = config("PTVSD_REMOTE_ADDRESS", default="0.0.0.0")
PTVSD_REMOTE_PORT = config("PTVSD_REMOTE_PORT", default=3000, cast=int)
PTVSD_WAIT_FOR_ATTACH = config("PTVSD_WAIT_FOR_ATTACH", default=False, cast=bool)

# Setup for debug_toolbar in dev only for admins

# Method to show the user, if they're authenticated and superuser
def show_debug_toolbar(request):
    return DEBUG and request.user and request.user.is_authenticated and request.user.is_superuser

if DEBUG:
    from debug_toolbar import settings as dt_settings
    DEBUG_TOOLBAR_PANELS = dt_settings.PANELS_DEFAULTS + ['cachalot.panels.CachalotPanel',]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK" : show_debug_toolbar,}
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Cache time to live
CACHALOT_TIMEOUT = config("CACHE_TTL", default=60 * 10, cast=int)

CACHE_OPTIONS = json.loads(config('CACHE_OPTIONS', default='{"CLIENT_CLASS": "django_redis.client.DefaultClient"}'))

# Configure a cache
CACHES = {
    "default": {
        "BACKEND": config('CACHE_BACKEND', default="django_redis.cache.RedisCache"),
        "LOCATION": config('CACHE_LOCATION', default="redis://student_explorer_redis:6379/1"),
        "OPTIONS": CACHE_OPTIONS,
        "KEY_PREFIX": config('CACHE_KEY_PREFIX', default="student_explorer"),
        "TIMEOUT": CACHALOT_TIMEOUT,
    }
}

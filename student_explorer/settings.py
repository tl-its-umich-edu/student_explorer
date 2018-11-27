"""
Django settings for student_explorer project.

By default the application does not use this module, it reads settings from
student_explorer.local.settings, create that module and add
    from student_explorer.settings import *
to the top, then override settings initialized in this module.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import getenv


def getenv_bool(var, default='0'):
    return getenv(var, default).lower() in ('yes', 'on', 'true', '1', )

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv_bool('DJANGO_DEBUG')
ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY', 'I need to be changed!')

SESSION_COOKIE_AGE = int(getenv('DJANGO_SESSION_COOKIE_AGE', 36000))
SESSION_SAVE_EVERY_REQUEST = getenv_bool('DJANGO_SESSION_SAVE_EVERY_REQUEST',
                                         'on')

SILENCED_SYSTEM_CHECKS = []

ADMINS = [('', getenv('DJANGO_ERROR_EMAIL', 'vagrant@localhost'))]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'watchman',
    'student_explorer',
    'seumich',
    'management',
    'tracking',
    'feedback',
    'usage',
)

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

USE_X_FORWARDED_HOST = getenv_bool('DJANGO_USE_X_FORWARDED_HOST', 'no')

FORCE_SCRIPT_NAME = getenv('DJANGO_FORCE_SCRIPT_NAME', None)

WATCHMAN_TOKEN = getenv('DJANGO_WATCHMAN_TOKEN', None)
WATCHMAN_TOKEN_NAME = getenv('DJANGO_WATCHMAN_TOKEN_NAME', 'token')

DOWNLOAD_TOKEN = getenv('DJANGO_DOWNLOAD_TOKEN', None)

PAGINATION_RECORDS_PER_PAGE = int(getenv(
    'DJANGO_PAGINATION_RECORDS_PER_PAGE', '10'))
PAGINATION_NUM_PAGE_LINKS = int(getenv(
    'DJANGO_PAGINATION_NUM_PAGE_LINKS', '5'))

SERVER_EMAIL = getenv('DJANGO_SERVER_EMAIL',
                      'student-explorer-admins@umich.edu')

USAGE_PAST_WEEKS = int(getenv(
    'DJANGO_USAGE_PAST_WEEKS', '8'))

# Internationalization

LANGUAGE_CODE = getenv('DJANGO_LANGUAGE_CODE', 'en-us')

TIME_ZONE = getenv('DJANGO_TIME_ZONE', 'America/Detroit')

USE_I18N = getenv_bool('DJANGO_USE_I18N', 'yes')

USE_L10N = getenv_bool('DJANGO_USE_L10N', 'yes')

USE_TZ = getenv_bool('DJANGO_USE_TZ', 'yes')


# Static files (CSS, JavaScript, Images)

STATIC_URL = getenv('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = getenv('DJANGO_STATIC_ROOT',
                     os.path.join(BASE_DIR, 'staticfiles'))

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = getenv('DJANGO_LOGIN_URL', '/accounts/login/')
LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = getenv('DJANGO_LOGOUT_REDIRECT_URL', '/')

EMAIL_HOST = getenv('DJANGO_EMAIL_HOST', 'localhost')
EMAIL_PORT = int(getenv('DJANGO_EMAIL_PORT', '25'))
EMAIL_HOST_USER = getenv('DJANGO_EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = getenv('DJANGO_EMAIL_HOST_PASSWORD', None)
EMAIL_USE_TLS = getenv('DJANGO_EMAIL_USE_TLS', None)
EMAIL_USE_SSL = getenv('DJANGO_EMAIL_USE_SSL', None)

FEEDBACK_EMAIL = getenv('DJANGO_FEEDBACK_EMAIL', None)

# Databases

DATABASES = {}
DATABASE_ROUTERS = []

DATABASES['default'] = {
    'ENGINE': getenv('DJANGO_DB_ENGINE', 'django.db.backends.mysql'),
    'NAME': getenv('DJANGO_DB_NAME', 'student_explorer'),
    'USER': getenv('DJANGO_DB_USER', 'student_explorer'),
    'PASSWORD': getenv('DJANGO_DB_PASSWORD', 'student_explorer'),
    'HOST': getenv('DJANGO_DB_HOST', ''),
    'PORT': getenv('DJANGO_DB_PORT', ''),
}

DATABASES['seumich'] = {
    'ENGINE': getenv('DJANGO_SEUMICH_DB_ENGINE', 'django.db.backends.mysql'),
    'NAME': getenv('DJANGO_SEUMICH_DB_NAME', 'student_explorer'),
    'USER': getenv('DJANGO_SEUMICH_DB_USER', 'student_explorer'),
    'PASSWORD': getenv('DJANGO_SEUMICH_DB_PASSWORD', 'student_explorer'),
    'HOST': getenv('DJANGO_SEUMICH_DB_HOST', ''),
    'PORT': getenv('DJANGO_SEUMICH_DB_PORT', ''),
    'MIGRATE': getenv_bool('DJANGO_SEUMICH_DB_MIGRATE', 'no'),

}
DATABASE_ROUTERS += ['seumich.routers.SeumichRouter']


# SAML Auth

if getenv_bool('STUDENT_EXPLORER_SAML'):
    SAML2_URL_PATH = getenv('STUDENT_EXPLORER_SAML_URL_PATH', '/accounts/')
    SAML2_URL_BASE = getenv('STUDENT_EXPLORER_SAML_URL_BASE',
                            'http://localhost:2082/accounts/')

    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'djangosaml2.backends.Saml2Backend',
    )
    LOGIN_URL = '%slogin/' % SAML2_URL_PATH
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    import saml2
    SAML_CONFIG = {
      'xmlsec_binary': '/usr/bin/xmlsec1',
      'entityid': '%smetadata/' % SAML2_URL_BASE,

      # directory with attribute mapping
      # 'attribute_map_dir': os.path.join(BASE_DIR, 'attribute-maps'),
      'name': getenv('STUDENT_EXPLORER_SAML_SERVICE_NAME', 'Student Explorer'),
      # this block states what services we provide
      'service': {
          # we are just a lonely SP
          'sp': {
              'name': 'Student Explorer',
              'name_id_format': getenv(
                'STUDENT_EXPLORER_SAML_NAME_ID_FORMAT',
                'urn:oasis:names:tc:SAML:2.0:nameid-format:transient'),
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

      # where the remote metadata is stored
      'metadata': {
          'local': [os.path.join(
            BASE_DIR, 'student_explorer/local/saml/remote-metadata.xml')],
          },

      # set to 1 to output debugging information
      'debug': 1,

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
            'level': getenv('DJANGO_LOGGING_LEVEL_EMAIL_ADMINS', 'ERROR'),
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
            'level': getenv('DJANGO_LOGGING_LEVEL_EMAIL_ADMINS', 'ERROR'),
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOGGING_LEVEL', 'WARNING'),
        },
        'se_umich': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOGGING_LEVEL', 'WARNING'),
        },
        'feedback': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOGGING_LEVEL', 'WARNING'),
        },
        'tracking': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOGGING_LEVEL', 'WARNING'),
        },
        'student_explorer': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOGGING_LEVEL', 'WARNING'),
        },
        'access_logs': {
            'handlers': ['access_logs'],
            'level': 'INFO',
        },
    },
}

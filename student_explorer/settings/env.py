from student_explorer.settings.base import *
from os import getenv


SECRET_KEY = getenv('DJANGO_SECRET_KEY', 'I need to be changed!')

HASHREDIRECT_ENABLED = bool(int(getenv('DJANGO_HASHREDIRECT_ENABLED', '0')))
HASHREDIRECT_LOGOUT_REDIRECT = getenv(
    'DJANGO_HASHREDIRECT_LOGOUT_REDIRECT', '0')

LOGIN_URL = getenv('DJANGO_LOGIN_URL', None)

DATABASES = {
    'default': {
        'ENGINE': getenv('DJANGO_DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': getenv('DJANGO_DB_NAME', 'student_explorer'),
        'USER': getenv('DJANGO_DB_USER', 'student_explorer'),
        'PASSWORD': getenv('DJANGO_DB_PASSWORD', 'student_explorer'),
        'HOST': getenv('DJANGO_DB_HOST', ''),
        'PORT': getenv('DJANGO_DB_PORT', ''),
    },
    'lt_dataset': {
        'ENGINE': getenv('DJANGO_LTDATA_DB_ENGINE',
                         'django.db.backends.oracle'),
        'NAME': getenv('DJANGO_LTDATA_DB_NAME', None),
        'USER': getenv('DJANGO_LTDATA_DB_USER', None),
        'PASSWORD': getenv('DJANGO_LTDATA_DB_PASSWORD', None),
        'HOST': getenv('DJANGO_LTDATA_DB_HOST', ''),
        'PORT': getenv('DJANGO_LTDATA_DB_PORT', ''),
        'TEST': {
            'MIRROR': 'default',
        },

    },
}

REST_FRAMEWORK['PAGE_SIZE'] = int(getenv('DJANGO_REST_FRAMEWORK_PAGE_SIZE', 0))

USE_ADVISING_DATABASE = bool(int(getenv('DJANGO_USE_LTDATA_DATABASE', False)))

if USE_ADVISING_DATABASE:
    ADVISING_DATABASE = 'lt_dataset'
    ADVISING_PACKAGE = 'advisingumich'
    INSTALLED_APPS += ('advisingumich',)
    DATABASE_ROUTERS = ['advisingumich.routers.DataWarehouseRouter']


REMOTE_USER_HEADER = getenv('DJANGO_REMOTE_USER_HEADER', None)

if REMOTE_USER_HEADER:
    MIDDLEWARE_CLASSES += (
        'umichuser.middleware.ProxiedRemoteUserMiddleware',
    )

    AUTHENTICATION_BACKENDS = (
        # 'django.contrib.auth.backends.RemoteUserBackend',
        'umichuser.backends.DigRemoteUserBackend',

    )

    LDAP = {
        'mcommunity': {
            'HOST': getenv('DJANGO_LDAP_HOST', 'ldap://ldap.umich.edu/'),
            'USER': getenv('DJANGO_LDAP_USER', None),
            'PASSWORD': getenv('DJANGO_LDAP_PASSWORD', None),
            'SEARCH_BASE': getenv('DJANGO_LDAP_SEARCH_BASE',
                                  'ou=People,dc=umich,dc=edu'),
            'CA_CERT_FILE': getenv('DJANGO_LDAP_CA_CERT_FILE', None),
        },
    }

# STATIC_ROOT = '/var/www/student_explorer/static'
USE_X_FORWARDED_HOST = bool(getenv('DJANGO_USE_X_FORWARDED_HOST', False))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = getenv('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = getenv('DJANGO_STATIC_ROOT', None)


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
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': getenv('DJANGO_LOGGING_LEVEL', 'WARNING'),
        },
    },
}

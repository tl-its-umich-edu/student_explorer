from settings.base import *

SECRET_KEY = 'I need to be changed! Get some random characters -->    head /dev/random | openssl base64'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_explorer',
        'USER': 'student_explorer',
        'PASSWORD': 'student_explorer',
        'HOST': '',
        'PORT': '',
    },
}


REMOTE_USER_HEADER = None
# REMOTE_USER_HEADER = 'HTTP_PROXY_USER'

if REMOTE_USER_HEADER:
    MIDDLEWARE_CLASSES += (
        'umichdig.middleware.ProxiedRemoteUserMiddleware',
    )

    AUTHENTICATION_BACKENDS = (
        # 'django.contrib.auth.backends.RemoteUserBackend',
        'umichdig.backends.DigRemoteUserBackend',

    )

    LDAP = {
        'mcommunity': {
            'HOST': 'ldap://ldap.umich.edu/',
            'USER': None,
            'PASSWORD': None,
            'SEARCH_BASE': 'ou=People,dc=umich,dc=edu',
            'CA_CERT_FILE': None,
        },
    }

STATIC_ROOT = '/var/www/student_explorer/static'

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
        # '': {
        #     'handlers': ['console'],
        #     'level': 'INFO',
        # },
        'umichdig': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

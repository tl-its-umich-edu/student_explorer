from settings.base import *

SECRET_KEY = 'I need to be changed!'
HASHREDIRECT_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_explorer',
        'USER': 'student_explorer',
        'PASSWORD': 'student_explorer',
        'HOST': '',
        'PORT': '',
    },
    # 'lt_dataset': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': 'pa07',
    #     'USER': 'steinhof',
    #     'PASSWORD': '',
    #     'HOST': 'crow.dsc.umich.edu',
    #     'PORT': '1521',
    # },
}

# ADVISING_DATABASE = 'lt_dataset'
# INSTALLED_APPS += (
#     'advisingumich',
# )
# ADVISING_PACKAGE = 'advisingumich'
# DATABASE_ROUTERS = ['advisingumich.routers.DataWarehouseRouter']


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

STATIC_ROOT = '/vagrant/sespa/app/static'

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

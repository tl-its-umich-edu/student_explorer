from student_explorer.settings.base import *
from os import getenv


def getenv_bool(var, default='0'):
    return getenv(var, default).lower() in ('yes', 'on', 'true', '1', )

DEBUG = getenv_bool('DJANGO_DEBUG')
ALLOWED_HOSTS += getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

SECRET_KEY = getenv('DJANGO_SECRET_KEY', 'I need to be changed!')

HASHREDIRECT_ENABLED = getenv_bool('DJANGO_HASHREDIRECT_ENABLED')
HASHREDIRECT_LOGOUT_REDIRECT = getenv(
    'DJANGO_HASHREDIRECT_LOGOUT_REDIRECT', '0')

LOGIN_URL = getenv('DJANGO_LOGIN_URL', None)

DATABASE_ROUTERS = []

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

# DATABASES['seumich'] = {
#     'ENGINE': getenv('DJANGO_SEUMICH_DB_ENGINE'),
#     'NAME': getenv('DJANGO_SEUMICH_DB_NAME'),
#     'USER': getenv('DJANGO_SEUMICH_DB_USER'),
#     'PASSWORD': getenv('DJANGO_SEUMICH_DB_PASSWORD'),
#     'HOST': getenv('DJANGO_SEUMICH_DB_HOST'),
#     'PORT': getenv('DJANGO_SEUMICH_DB_PORT'),
# }
# DATABASE_ROUTERS += ['seumich.routers.SeumichRouter']

REST_FRAMEWORK['PAGE_SIZE'] = int(getenv('DJANGO_REST_FRAMEWORK_PAGE_SIZE', 0))

USE_ADVISING_DATABASE = getenv_bool('DJANGO_USE_LTDATA_DATABASE')

if USE_ADVISING_DATABASE:
    ADVISING_DATABASE = 'lt_dataset'
    ADVISING_PACKAGE = 'advisingumich'
    INSTALLED_APPS += ('advisingumich',)
    DATABASE_ROUTERS = ['advisingumich.routers.DataWarehouseRouter']

if getenv_bool('STUDENT_EXPLORER_SAML'):
    SAML2_URL_PATH = getenv('STUDENT_EXPLORER_SAML_URL_PATH', '/saml2/')
    SAML2_URL_BASE = getenv('STUDENT_EXPLORER_SAML_URL_BASE',
                            'http://localhost:2082/saml2/')

    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'djangosaml2.backends.Saml2Backend',
    )
    LOGIN_URL = '%slogin/' % SAML2_URL_PATH
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    from os import path
    import saml2
    BASEDIR = path.dirname(path.abspath(__file__))
    SAML_CONFIG = {
      'xmlsec_binary': '/usr/bin/xmlsec1',
      'entityid': '%smetadata/' % SAML2_URL_BASE,

      # directory with attribute mapping
      # 'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
      'name': getenv('STUDENT_EXPLORER_SAML_SERVICE_NAME', 'Student Explorer'),
      'valid_for': 48,

      # this block states what services we provide
      'service': {
          # we are just a lonely SP
          'sp': {
              'valid_for': 48,
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
          'local': [path.join(BASEDIR, '../saml/remote_metadata.xml')],
          },

      # set to 1 to output debugging information
      'debug': 1,

      # certificate
      'key_file': path.join(BASEDIR, '../saml/key.pem'),  # private part
      'cert_file': path.join(BASEDIR, '../saml/cert.pem'),  # public part

      'valid_for': 24,  # how long is our metadata valid
      }


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
USE_X_FORWARDED_HOST = getenv_bool('DJANGO_USE_X_FORWARDED_HOST')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = getenv('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = getenv('DJANGO_STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))


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

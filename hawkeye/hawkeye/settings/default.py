"""
Django settings for hawkeye project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#m4)%9nsi)690zjmdkpz2=_y^&48x749ir+4&z@!+(6tvxd0ih'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'guardian',
    #apps
    'authx',
    'common',
    'api',
    'monitor',
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

ROOT_URLCONF = 'hawkeye.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'hawkeye.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "onedream",
        'USER': "yunqu",
        'PASSWORD': "yunqu",
        'HOST': "127.0.0.1",
        },
    }

# celery + redis
# Keep consistent with /etc/redis.conf 'requirepass' config
# please DO redefine `BROKER_URL` in ${env}.py if above properties change
REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = ''
REDIS_MULE_DB = 0

REDIS_CONFIG = {
    'password': REDIS_PASSWORD,
    'port': REDIS_PORT,
    'host': REDIS_HOST,
}
REDIS_CONN_STR = 'redis://:%(password)s@%(host)s:%(port)s/0' % REDIS_CONFIG

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONN_STR,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
            }
        }
    }
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

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', # for the time being only
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'authx.authentication.CsrfExemptSessionAuthentication',
        'authx.authentication.JSONWebTokenAuthenticationQS',    # almost for debug only
    ),
    # this should align the same as django GenericListView paginate_by, page_size mechanism
    'DEFAULT_FILTER_BACKENDS': (
                                #'url_filter.integrations.drf.DjangoFilterBackend',
                                #'rest_framework.filters.DjangoFilterBackend',
                                #'django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework_filters.backends.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter',
                                #'rest_framework.filters.OrderingFilter',
                                'common.filters.RelatedOrderingFilter'),
    'SEARCH_PARAM': 'q',
    'ORDERING_PARAM': 'ordering',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPagination',
    'PAGE_SIZE': 10,
    #'PAGE_QUERY_PARAM': 'page', # sadly no this config, 'page' already is the default query param for this PageNumberPagination
    #'PAGINATE_BY_PARAM': 'page_size', # this is also in REMOVED_SETTINGS
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DATETIME_INPUT_FORMATS': ["%Y-%m-%d %H:%M:%S", ]

}

QS_JWT_KEY = 'jwt' # for authx.authentication to parse query_params if any jwt

AUTH_USER_MODEL = 'authx.User'

JWT_AUTH = {
    # 'JWT_PAYLOAD_HANDLER': 'authx.utils.jwt_payload_handler',  # we should make the payload count
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'authx.utils.jwt_response_payload_handler',
    #'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

    # default stuff with comments no more doc looking up
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 60,  # in seconds
    # This allows you to validate an expiration time which is in the past but no very far.
    # For example, if you have a JWT payload with an expiration time set to 30 seconds after creation
    # but you know that sometimes you will process it after 30 seconds,
    # you can set a leeway of 10 seconds in order to have some margin
    'JWT_AUDIENCE': None,
# This is a string that will be checked against the aud field of the token, if present. Default is None(fail if aud present on JWT).
    'JWT_ISSUER': None,
# This is a string that will be checked against the iss field of the token. Default is None(do not check iss on JWT).

    'JWT_ALLOW_REFRESH': True,
# Enable token refresh functionality. Token issued from rest_framework_jwt.views.obtain_jwt_token will have an orig_iat field.
    # for usage clarification of the following two options
    # plz refer to https://github.com/GetBlimp/django-rest-framework-jwt/issues/92#issuecomment-227763338
    # in this situation, once the user is forced to log off, you will have to login again with username/password
    # if you want the user stay logon for a really long time(which is not good), you might as well set the JWT_EXPIRATION_DELTA long enough, but JWT_EXPIRATION_DELTA<JWT_REFRESH_EXPIRATION_DELTA for sure
    'JWT_EXPIRATION_DELTA': timedelta(days=1),
# used to be seconds=300, original should be no longer than JWT_REFRESH_EXPIRATION_DELTA
    # as recommended @http://stackoverflow.com/questions/26739167/jwt-json-web-token-automatic-prolongation-of-expiration?rq=1
    # a generic JWT_EXPIRATION_DELTA would be 1 hour, renew should go with every time user open the page and one hour with a setTimeout(maybe?)
    # and JWT_REFRESH_EXPIRATION_DELTA should be 1 week
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),  # Limit on token refresh, is a datetime.timedelta instance.
    # This is how much time after the original token that future tokens can be refreshed from.
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # that HTTP Header Authorization: Bearer xxx, Bearer part
}

PROJECT_LOG_DIR = os.path.join(BASE_DIR, '..', 'quicksilver-logs')
if not os.path.exists(PROJECT_LOG_DIR):
    os.makedirs(PROJECT_LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'filename': os.path.join(PROJECT_LOG_DIR, 'app.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'db_debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['require_debug_true'],
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filename': os.path.join(PROJECT_LOG_DIR, 'db.log'),
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'django.request': {
            # 'handlers': ['file', 'mail_admins'],
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['db_debug', 'console', ],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

'''
form based auth settings
'''
LOGIN_URL = '/authx/login/'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

BASE_URL = "http://127.0.0.1:8080/"

ANONYMOUS_USER_NAME = 'Anonymous'

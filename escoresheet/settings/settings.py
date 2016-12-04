"""
Django settings for escoresheet project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

import pytz
from django.core.urlresolvers import reverse_lazy

SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ESCORESHEET_MODULE_ROOT = os.path.join(BASE_DIR, 'escoresheet')
NODE_MODULES_ROOT = os.path.join(BASE_DIR, 'node_modules')

# Custom django apps are in apps/ directory, so add it to path
sys.path.append(os.path.join(BASE_DIR, 'apps'))

ADMINS = [('Harris', 'hpittin1@binghamton.edu'), ]
MANAGERS = ADMINS

# TODO add caching (redis or memcached)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

# TODO See warning on https://docs.djangoproject.com/en/1.9/ref/settings/#secure-proxy-ssl-header. Need to have proxy strip X-Forwarded-Proto header and then set it myself so nobody can spoof the header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# TODO regenerate new key, export as env var on servers
# SECURITY WARNING: keep the secret key used in production secret!
DEV_KEY = '9(31c+k9q8p++7a46ite17(@a3os_*)gg@+yqn4_5isb^v5=tr'
SECRET_KEY = os.environ.get('SECRET_KEY', DEV_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

# TODO move dev/test only dependencies to correct settings files, requirements files
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd party apps
    'debug_toolbar',
    'djangobower',
    'django_extensions',
    'compressor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'behave_django',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    # custom apps
    'home.apps.HomeConfig',
    'accounts.apps.AccountsConfig',
    'userprofiles.apps.UserprofilesConfig',
    'sports.apps.SportsConfig',
    'leagues.apps.LeaguesConfig',
    'divisions.apps.DivisionsConfig',
    'teams.apps.TeamsConfig',
    'coaches.apps.CoachesConfig',
    'managers.apps.ManagersConfig',
    'referees.apps.RefereesConfig',
    'players.apps.PlayersConfig',
    'seasons.apps.SeasonsConfig',
    'api.apps.ApiConfig',
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'escoresheet.middleware.TranslationMiddleware',
    'escoresheet.middleware.TimezoneMiddleware',
    'accounts.middleware.AccountAndSportRegistrationCompleteMiddleware'
]

ROOT_URLCONF = 'escoresheet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'escoresheet.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# TODO setup postgres, see if postgres can read username, etc. from file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'prod_db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

COMMON_TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]

USE_I18N = True

USE_L10N = True

USE_TZ = True

# TODO look into rotating file handler
# TODO add in other needed loggers to files and add in any useful django custom logger formatters, etc.
# https://docs.python.org/3.4/library/logging.handlers.html
# https://docs.djangoproject.com/en/1.9/topics/logging/#django-s-logging-extensions

DJANGO_LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(DJANGO_LOGS_DIR):
    os.mkdir(DJANGO_LOGS_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(pathname)s:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console_simple': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_verbose': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_verbose': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(DJANGO_LOGS_DIR, 'server_log.log'),
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': [],
            'include_html': True,
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            'filters': ['require_debug_true'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_simple'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['file_verbose', 'console_verbose'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

# Email address admins/managers receive mail from
# TODO change this
SERVER_EMAIL = 'root@localhost'

# Email address regular users receive mail from
# TODO change this
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# TODO configure this for prod
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
# Only set one of these to True at a time, if have problems try setting the other one
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Http requests to STATIC_URL should be mapped to STATIC_ROOT

# The actual uri staticfiles are served from (localhost:8000/static/)
STATIC_URL = '/static/'
# The folder on the filesystem staticfiles are stored
STATIC_ROOT = os.path.join(BASE_DIR, 'production_static')
# Location to find extra static files (Django automatically looks in static/ subdirectories of all apps)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_FINDERS = ['django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'djangobower.finders.BowerFinder',
                       'compressor.finders.CompressorFinder'
                       ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Django bower related
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, '', 'static')
BOWER_PATH = os.path.join(NODE_MODULES_ROOT, 'bower/bin/bower')
BOWER_INSTALLED_APPS = [
    'animate.css#3.5.2',
    'bootstrap-sass',
    'font-awesome#4.6.3',
    'jquery#2.2.4',
    'noty#2.3.8',
    'bootstrap-select'
]

# Django compressor related
# TODO add in other minifiers, etc. for scss, css, js. Look into settings for yuglify
COMPRESS_PRECOMPILERS = [('text/scss', 'sassc {infile} {outfile} -p 8')]
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',
                        'compressor.filters.yuglify.YUglifyCSSFilter',
                        'django_compressor_autoprefixer.AutoprefixerFilter']
COMPRESS_YUGLIFY_BINARY = os.path.join(NODE_MODULES_ROOT, 'yuglify/bin/yuglify')
COMPRESS_JS_FILTERS = ['compressor.filters.yuglify.YUglifyJSFilter']
COMPRESS_AUTOPREFIXER_BINARY = os.path.join(NODE_MODULES_ROOT, 'postcss-cli/bin/postcss')
COMPRESS_AUTOPREFIXER_ARGS = '--use autoprefixer -c {}'.format(os.path.join(BASE_DIR, 'post_css_config.json'))
COMPRESS_ROOT = STATICFILES_DIRS[0]

# User account related

# Django all auth
# TODO look at django all auth settings again to see if missing any settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.SignupForm',
    'login': 'accounts.forms.LoginForm',
    'reset_password': 'accounts.forms.PasswordResetForm',
    'reset_password_from_key': 'accounts.forms.PasswordResetFromKeyForm',
    'change_password': 'accounts.forms.ChangePasswordForm',
    'add_email': 'accounts.forms.AddEmailForm'
}
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_USER_DISPLAY = lambda user: user.email

# Django auth settings
LOGIN_URL = reverse_lazy('account_login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('account_logout')

TEST_RUNNER = 'redgreenunittest.django.runner.RedGreenDiscoverRunner'

FIXTURE_DIRS = [
    os.path.join(ESCORESHEET_MODULE_ROOT, 'fixtures')
]

API_VERSIONS = ['v1']
DEFAULT_VERSION = 'v1'

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': DEFAULT_VERSION,
    'ALLOWED_VERSIONS': API_VERSIONS,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # For local development, BasicAuthentication is appended to this list in local_settings.py.dev
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

# TODO run through Django settings docs again to see if missing any settings

try:
    # Running in dev mode
    from .local_settings import *
except ImportError as e:
    # Running in production mode
    pass
finally:
    # Running in testing mode
    if len(sys.argv) > 1 and ('test' in sys.argv or 'behave' in sys.argv):
        from .testing_settings import *

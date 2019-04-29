# XXX - bring back default comments to this file...
import os

pdsDefaultLocation = "localhost:5000"
SERVER_UPLOAD_DIR = '/var/www/trustframework/'

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        # supported db backends are 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'
        #'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': '/var/www/trustframework/registryEnv/OMS-RegistryServer/test.db',
        'NAME': 'test.db',
        'USER': 'default',
        'PASSWORD': 'default',
        'HOST': '',
        'PORT': '',
#	'OPTIONS': {
#		'read_default_file': '/etc/mysql/my.cnf',
#		},
    }
}

# where can we find db fixtures?
FIXTURE_DIRS = (
   os.path.join(PROJECT_DIR, 'apps/account/fixtures'),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# when auth is required, django will redirect here
LOGIN_URL = "/Shibboleth.sso/Login"

# after a successful login, django will redirect here
LOGIN_REDIRECT_URL = "/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static_collection')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
# Don't forget to use absolute paths, not relative paths, and use forward slashes
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
# XXX - we'll need to figure out a sensible way to regenerate this on deployment
SECRET_KEY = 'shfkjs894fFerER#5h346&25hjkfbc2=23_6817A1lh[dfjg3=_-89j'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
#    'django.contrib.auth.backends.RemoteUserBackend',
 'shibboleth.backends.ShibbolethRemoteUserBackend',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

# where to look for templates
# Don't forget to use absolute paths, not relative paths, and use forward slashes
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', #Currently CSRF forgery protection is turned off
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Python dotted path to the WSGI application used by Django's runserver.
#WSGI_APPLICATION = 'registryServer.wsgi.application'

ROOT_URLCONF = 'urls'

# Define user profile associated with a User
AUTH_PROFILE_MODULE = 'account.Profile'

SHIBBOLETH_ATTRIBUTE_MAP = {
   "HTTP_REMOTE_USER": (True, "username"),
#   "Shibboleth-givenName": (False, "first_name"),
#   "Shibboleth-sn": (False, "last_name"),
   "HTTP_MAIL": (True, "email"),
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sites',
    'apps.base',
    'apps.client',
    'apps.account',
    'apps.oauth2',
    'apps.questions',
    'uni_form',
    'oauth2app',
    'django_extensions',
    'lib',
#    'shibboleth',
    )

import logging
import sys
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#    'regisryServer.apps.oauth2',
# XXX - look up to confirm this is correct
# TTL for an OAUTH2 access token, in seconds (presumably)
OAUTH2_ACCESS_TOKEN_EXPIRATION = 36000000

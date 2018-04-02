# Django settings for the Claremont Humans versus Zombies project.

import datetime
import os

import markdown

from django.utils import timezone, html

from root import PROJECT_PATH
import local_settings

### The following settings should all be defined in a file called
### "local_settings.py".

# A list of hostnames from which this site can serve. Used in production.
ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS or []

# Do you want the site to display a bunch of information when
# something goes wrong? Either True or False.
DEBUG = local_settings.DEBUG

# Similar to DEBUG, but for template errors. Also either True or
# False.
TEMPLATE_DEBUG = local_settings.TEMPLATE_DEBUG

# A list of the people with admin access, along with their email
# addresses. It should look something like the following:

# ADMINS = (
#     # ('Your Name', 'your_email@domain.com'),
# )

ADMINS = local_settings.ADMINS
MANAGERS = ADMINS

# Does your email service use TLS? True or False.
EMAIL_USE_TLS = local_settings.EMAIL_USE_TLS

# What host does your email service use? We use "smtp.gmail.com"
EMAIL_HOST = local_settings.EMAIL_HOST

# Your email username and password. We're not telling you ours ;)
EMAIL_HOST_USER = "hvzwattest4@gmail.com" #local_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = "claremonthvz4" #local_settings.EMAIL_HOST_PASSWORD

# Your email service's port number. Ours is 587.
EMAIL_PORT = local_settings.EMAIL_PORT

# Make this unique, and don't share it with anybody. Any string will
# do, but this tool works well:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = local_settings.SECRET_KEY

# List your databases here!

# DATABASES = {
#     'default': {
#
#         'ENGINE': 'django.db.backends.mysql', # Add
#                                               # 'postgresql_psycopg2',
#                                               # 'postgresql', 'mysql',
#                                               # 'sqlite3' or 'oracle'.
#
#         'NAME': 'claremontHvZ_django',        # Or path to database
#                                               # file if using sqlite3.
#
#         'USER': 'me',                         # Not used with sqlite3.
#
#         'PASSWORD': 'secret',                 # Not used with sqlite3.
#
#         'HOST': '127.0.0.1',                  # Set to empty string
#                                               # for localhost. Not
#                                               # used with sqlite3.
#
#         'PORT': '',                           # Set to empty string
#                                               # for default. Not used
#                                               # with sqlite3.
#     }
# }
DATABASES = local_settings.DATABASES


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/Los_Angeles"


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

CACHES = local_settings.CACHES

### We're done here! ###

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'upload-media')
HUMAN_PICS = os.path.join(MEDIA_ROOT, 'human_pics')
ZOMBIE_PICS = os.path.join(MEDIA_ROOT, 'zombie_pics')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/upload-media/'

# Specify where images, scripts, and compiled stylesheets should go.
STATIC_ROOT = getattr(
    local_settings,
    'STATIC_ROOT',
    os.path.join(PROJECT_PATH, "static")
)

# Specify the root URL for images, scripts, and compiled stylesheets.
STATIC_URL = "/static/"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# List of callables that know how to import templates from various sources.

TEMPLATE_LOADERS = (
    (
        'django.template.loaders.cached.Loader',
        (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
    ),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'HVZ.main.middleware.Http403Middleware',
)

AUTHENTICATION_BACKENDS = (
    'HVZ.main.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'HVZ.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on
    # Windows.  Don't forget to use absolute paths, not relative
    # paths.
    os.path.join(PROJECT_PATH, "HVZ", "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "HVZ.main.context_processors.inject_outbreak_percentage",
    "HVZ.main.context_processors.inject_current_player",
    "HVZ.main.context_processors.inject_mod_info",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'longerusernameandemail',

    'widget_tweaks',

    'HVZ.main',
    'HVZ.feed',
    'HVZ.players',
    'HVZ.rules',
    'HVZ.missions',
    'HVZ.stats',
    'HVZ.forum',
    'HVZ.api',
)

# App-specific settings below:

# Verbose names for the teams
VERBOSE_TEAMS = {
    'H': "Humans",
    'Z': "Zombies",
    'B': "Both Teams",
}

# The length of a feed code.
FEED_LEN = 5

# The characters we allow in a feed code.
VALID_CHARS = ["A", "C", "E", "L", "X", "N", "P", "O", "S", "T", "W", "Z"]

MARKUP_FIELD_TYPES = (
    ('markdown', lambda markup: markdown.markdown(html.urlize(markup))),
    ('plain', lambda markup: html.urlize(html.linebreaks(markup))),
)

# The times corresponding to the beginning of "day" and "night". Used
# for missions.
START_TIMES = {
    'D': datetime.time(hour=7),
    'N': datetime.time(hour=17),
}

WSGI_APPLICATION = 'passenger_wsgi.application'

MOD_PHONE_NUMBER = "909-555-5555"


MODERATOR_EMAIL = "moderator@claremonthvz.org"
ANON_HARRASSMENT_EMAIL = "hvzanonymouscomplaint@gmail.com"

# Callables that return the "current" date and time.
# Can be overridden in local_settings or tests to return a fixed point in time.
NOW = local_settings.NOW or timezone.now


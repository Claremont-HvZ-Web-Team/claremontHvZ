# Django settings for the Claremont Humans versus Zombies project.

import os
import local_settings

### The following settings should all be defined in a file called
### "local_settings.py".

# The absolute root of your app's home directory, something like
# "/home/claremontHvZ/claremonthvz.org/"
PROJECT_PATH = local_settings.PROJECT_PATH

def absolute_path(path):
    return os.path.join(PROJECT_PATH, path)

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
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD

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

# We live in Claremont, so ours is "America/Los_Angeles".
TIME_ZONE = local_settings.TIME_ZONE


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

# Ours is "en-us"
LANGUAGE_CODE = local_settings.LANGUAGE_CODE

### We're done here! ###

CACHE_BACKEND = "file://" + absolute_path('cache')

MANAGERS = ADMINS

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

#This is a new setting in Django 1.4. If you use timezone aware shenanigans everything breaks.
USE_TZ = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = absolute_path('public/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# List of callables that know how to import templates from various sources.

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        )),
)

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'DjangoProject.urls'

TEMPLATE_DIRS = (
    absolute_path('templates'),
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on
    # Windows.  Don't forget to use absolute paths, not relative
    # paths.
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # 'tinymce',
    'HvZ',
    'django.contrib.flatpages',
)

### GAME SPECIFIC THINGS GO HERE.

# The Google doc containing rules information.
RULES_DOC_LINK = "https://docs.google.com/document/d/1PH-KEV9mp82Gn9kggDZx20RHuWgR64ubjc83BZi698g"

# The Google doc containing mission information.
MISSION_DOC_LINK = "https://docs.google.com/document/d/1CXWBrwvWLoMcP5zDgT_4YcB8NfRgo8oK3UMIcmNJ-s4"

MODERATOR_EMAIL = "mod@claremonthvz.org"
ANON_HARRASSMENT_EMAIL = "hvzanonymouscomplaint@gmail.com"

# The length of a feed code.
FEED_LEN = 5

# The characters we allow in a feed code.
VALID_CHARS = ["A", "C", "E", "L", "N", "O", "P", "S", "T", "W", "X", "Z"]

from django.utils import timezone
NOW = lambda: timezone.now()

### The following settings should all be defined in a file called
### "local_settings.py".
from hvz import local_settings

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
EMAIL_HOST_USER = "hvzwattest@gmail.com"
EMAIL_HOST_PASSWORD = "claremonthvz"

# Your email service's port number. Ours is 587.
EMAIL_PORT = local_settings.EMAIL_PORT

# Make this unique, and don't share it with anybody. Any string will
# do, but this tool works well:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = local_settings.SECRET_KEY

### TECHNICAL STUFF BELOW

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'hvz.main',
    'hvz.api',
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

ROOT_URLCONF = 'hvz.urls'

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
                'hvz.main.context_processors.inject_outbreak_percentage',
                'hvz.main.context_processors.inject_current_player',
            ],
        },
    },
]

WSGI_APPLICATION = 'hvz.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

DATABASES = local_settings.DATABASES

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = local_settings.STATIC_ROOT

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
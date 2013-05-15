# Machine-specific Django settings for the Claremont HvZ project.

import datetime
import os

# The absolute root of your app's home directory, something like
# "/home/claremontHvZ/claremonthvz.org/"
VIRTUALENV_DIR = os.path.join("/", "home", "MYUSERNAME", "MYPATH", "claremonthvz.org")

# The directory containing manage.py.
PROJECT_PATH = os.path.join(VIRTUALENV_DIR, "site", "claremontHvZ", "HVZ")

ALLOWED_HOSTS = None

# Do you want the site to display a bunch of information when
# something goes wrong?
DEBUG = True

# Similar to DEBUG, but for template errors.
TEMPLATE_DEBUG = DEBUG

# A list of the people with admin access, along with their email
# addresses. In production (where DEBUG is set to False), these people
# will receive emails every time something bad happens to the site.

ADMINS = (
    ('Hugh Mann', 'hmann@gmail.com'),
)

# Does your email service use TLS? True or False.
EMAIL_USE_TLS = True

# What host does your email service use? We use "smtp.gmail.com"
EMAIL_HOST = "smtp.gmail.com"

# Your email username and password. We're not telling you ours ;)
EMAIL_HOST_USER = "hmann@gmail.com"
EMAIL_HOST_PASSWORD = "hunter2"

# Your email service's port number. Ours is 587.
EMAIL_PORT = 587

# Make this unique, and don't share it with anybody. Any string will
# do, but this tool works well:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ")(#$(#$58OI$u50oIJ$#%9kw4j5kkKJE9#$%9*$WUJtui4up9"

# List your databases here! For development, sqlite3 is probably sufficient.

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.sqlite3', # Add
                                                # 'postgresql_psycopg2',
                                                # 'postgresql',
                                                # 'mysql', 'sqlite3'
                                                # or 'oracle'.

        'NAME': os.path.join(VIRTUALENV_DIR, 'site', 'hvz.sqlite3'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

# We live in Claremont, so ours is "America/Los_Angeles".
TIME_ZONE = "America/Los_Angeles"


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = "en-us"

# Specify your caching solution here. For development, the DummyCache
# class is fine.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

# Specify where images, scripts, and compiled stylesheets should go.
STATIC_ROOT = os.path.join(VIRTUALENV_DIR, "site", "static")

# Specify the root URL for images, scripts, and compiled stylesheets.
STATIC_URL = "/static/"

# The phone number associated with our phone service.
MOD_PHONE_NUMBER = "909-555-5555"

# You can set the app to a specific time here (useful for testing,
# since so much of the app is time-dependent). If this is set to
# "None", the app will instead use the current time.

#Right now, the time is fixed to 4/2/2013 2:00:00 PM.
NOW = lambda: datetime.datetime(2013, 04, 2, 14, 00, 00)

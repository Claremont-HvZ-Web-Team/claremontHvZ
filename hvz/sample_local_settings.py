# Machine-specific Django settings for the Claremont HvZ project.

import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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

        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Specify your caching solution here. For development, the DummyCache
# class is fine.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

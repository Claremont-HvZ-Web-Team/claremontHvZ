import os

PROJECT_PATH = "/home/jeff/hvz-site/new/claremonthvz.org/"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeff Hemphill', 'jthemphill@gmail.com')
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'web@claremonthvz.org'
EMAIL_HOST_PASSWORD = 'humansagainstzombies'
EMAIL_PORT = 587

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xv4oj_$3n9s9z8kfu9!$*ujvnf6(ha34v01$9x)zt)bpd)i8+7'

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.sqlite3', # Add
                                                # 'postgresql_psycopg2',
                                                # 'postgresql',
                                                # 'mysql', 'sqlite3'
                                                # or 'oracle'.

        'NAME': os.path.join(PROJECT_PATH, "development.db"),

        'USER': '',                         # Not used with sqlite3.

        'PASSWORD': '',                 # Not used with sqlite3.

        'HOST': '',                  # Set to empty string
                                              # for localhost. Not
                                              # used with sqlite3.

        'PORT': '',                           # Set to empty string
                                              # for default. Not used
                                              # with sqlite3.
    }
}

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

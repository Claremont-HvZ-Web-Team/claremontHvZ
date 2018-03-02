"""
Function get_custom_connection allow to select which email connection
to use for sending the email message.

Without `name` argument `get_custom_connection` function returns
default email connection built with `settings.EMAIL_*` settings:

* https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

If you pass `name` argument to that function then it will build
email connection with settings from `settings.EMAIL_CONNECTIONS[name]`

Exmaple of custom config::

    EMAIL_CONNECTIONS = {
        'gmail': {
            'host': 'smtp.gmail.com',
            'port': 587,
            'username': 'xxx@gmail.com',
            'password': 'xxx',
            'use_tls': True,
        },

Note that you shuld use "username" and "password" keys (not "host_user" and
"host_password" as you could think looking on `settings.EMAIL_*` options)
"""
from django.conf import settings
import django.core.mail


class MissingConnectionException(Exception):
    pass


def get_custom_connection(name=None, **kwargs):
    """
    If name is None return default email connection else
    build connection with settings from settings.EMAIL_CONNECTIONS[name]

    Args:
        name: key in settings.EMAIL_CONNECTIONS
    """

    if name is None:
        options = {}
    else:
        try:
            options = getattr(settings, 'EMAIL_CONNECTIONS')[name]
        except KeyError, AttributeError:
            raise MissingConnectionException(
                'Settings for email connection "%s" were not found' % label)

    options.update(kwargs)
    return django.core.mail.get_connection(**options)

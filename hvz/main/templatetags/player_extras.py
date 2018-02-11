from django.conf import settings
from django.template import Library

from hvz.main import models

register = Library()

@register.filter
def as_player(user):
    try:
        return models.Player.user_to_player(user)
    except models.Player.DoesNotExist:
        return ""

@register.filter
def filter_by(qs, keyvalue):
    key, value = keyvalue.split(',')
    return qs.filter(**{key: value})

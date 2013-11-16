from django.template import Library
from django.conf import settings

from HVZ.main.models import Player

register = Library()


@register.filter
def as_player(user):
    try:
        return Player.user_to_player(user)
    except Player.DoesNotExist:
        return ""


@register.filter
def team_name(team):
    return settings.VERBOSE_TEAMS[team]


@register.filter
def upgrade_name(upgrade):
    if not upgrade:
        return ""
    return Player.UPGRADES.get(upgrade, '')


@register.filter
def filter_by(qs, keyvalue):
    key, value = keyvalue.split(',')
    return qs.filter(**{key: value})

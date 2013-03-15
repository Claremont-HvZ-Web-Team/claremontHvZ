from django.template import Library

from HVZ.main.models import Player

register = Library()


@register.filter
def as_player(user):
    try:
        return Player.user_to_player(user)
    except:
        return ""


@register.filter
def team_name(team):
    return Player.TEAMS[team]


@register.filter
def upgrade_name(upgrade):
    if not upgrade:
        return ""
    return Player.UPGRADES.get(upgrade, '')


@register.filter
def filter_by(qs, keyvalue):
    key, value = keyvalue.split(',')
    print "filtering by {}: {}".format(key, value)
    return qs.filter(**{key: value})

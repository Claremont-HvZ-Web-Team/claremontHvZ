from django.template import Library

from HVZ.main.models import Player

register = Library()


@register.filter
def as_player(user):
    try:
        return Player.user_to_player(user)
    except:
        return ""

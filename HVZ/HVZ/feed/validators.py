from datetime import datetime

from django.core.exceptions import ValidationError
from django.conf import settings

from HVZ.main import utils

def ensure_human(player):
    if player.team != "H":
        raise ValidationError("{} is not a human!".format(player))

def ensure_zombie(player):
    if player.team != "Z":
        raise ValidationError("{} is not a zombie!".format(player))

def human_with_code(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not utils.current_players().filter(feed=feedcode).exists():
        raise ValidationError(
            "{} does not correspond to a player in this game.".format(feedcode))

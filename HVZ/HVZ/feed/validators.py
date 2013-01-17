from datetime import datetime

from django.core.exceptions import ValidationError

from HVZ.main.models import Player
from HVZ.main.utils import current_players

def ensure_human(player):
    if player.team != "H":
        raise ValidationError("{} is not a human!".format(player))

def ensure_zombie(player):
    if player.team != "Z":
        raise ValidationError("{} is not a zombie!".format(player))

def feedcode_human(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not current_players().filter(feed=feedcode).exists():
        raise ValidationError(
            "{} does not correspond to a player in this game.".format(feedcode))

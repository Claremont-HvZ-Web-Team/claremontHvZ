from datetime import datetime

from django.core.exceptions import ValidationError
from django.conf import settings

from HVZ.main import utils

def human_with_code(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not utils.current_players().filter(team="H", feed=feedcode).exists():
        raise ValidationError(
            "{} does not correspond to a player in this game.".format(feedcode))

from django.core.exceptions import ValidationError

from HVZ.main.models import Player


def human_with_code(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not Player.current_players().filter(team="H", feed=feedcode).exists():
        raise ValidationError(
            "{} doesn't correspond to a playing human!".format(feedcode))

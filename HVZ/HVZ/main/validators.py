from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

# Can't import specific names because circular import!
import models


def validate_chars(feedcode):
    """Raise an exception if we contain unapproved characters."""
    for c in feedcode:
        if c not in settings.VALID_CHARS:
            raise ValidationError(u"{} is not a valid character.".format(c))

def validate_past(time):
    """Ensure that the given time is in the past."""
    if time > datetime.now():
        raise ValidationError(u"{} must be in the past.".format(time))


class DateValidator:
    def __init__(self, game=None):
        if game is None:
            self.lazy_game = models.Game.imminent_game
        else:
            self.lazy_game = lambda: game

    def __call__(self, date):
        """Ensures that the given date is within the game's boundaries."""
        game = self.lazy_game()

        if date < game.start_date:
            raise ValidationError(
                u"The {} game started on {}. This date is {}.".format(
                    game,
                    game.start_date,
                    date
                ))

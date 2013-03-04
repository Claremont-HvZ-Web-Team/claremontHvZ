from django.conf import settings
from django.core.exceptions import ValidationError

# Can't import specific names because circular import!
import models


def validate_chars(feedcode):
    """Raise an exception if we contain unapproved characters."""
    for c in feedcode:
        if c not in settings.VALID_CHARS:
            raise ValidationError(u"{} is not a valid character.".format(c))

class TimeValidator:
    def __init__(self, game=None):
        if game is None:
            self.lazy_game = models.Game.imminent_game
        else:
            self.lazy_game = lambda: game

    def __call__(self, time):
        """Ensures that the given time is between our start date and now."""
        game = self.lazy_game()

        if time > settings.NOW():
            raise ValidationError(u"{} must be in the past.".format(time))

        if time.date() < game.start_date:
            raise ValidationError(
                u"The {} game started on {}. This date is {}.".format(
                    game,
                    game.start_date,
                    time.date()
                ))

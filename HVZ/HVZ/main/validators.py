from django.conf import settings
from django.core.exceptions import ValidationError

from utils import current_game

def feedcode_human(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not utils.current_players().filter(feed=feedcode).exists():
        raise ValidationError(
            "{} does not correspond to a player in this game.".format(feedcode))

def validate_chars(feedcode):
    """Raise an exception if we contain unapproved characters."""
    for c in feedcode:
        if c not in settings.VALID_CHARS:
            raise ValidationError(u"{} is not a valid character!".format(c))

class TimeValidator:
    def __init__(self, game=None):
        if game is None:
            game = current_game()

        self.game = game

    def __call__(self, time):
        """Ensures that the given time is between our start date and now."""
        if time > datetime.now():
            raise ValidationError(u"{} must be in the past.".format(time))

        if time.date < self.game.start_date:
            raise ValidationError(
                u"Game {} started on {}. This field is {}").format(
                self.game,
                self.game.start_date,
                time)

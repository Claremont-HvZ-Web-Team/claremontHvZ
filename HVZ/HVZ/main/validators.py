from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

import models

from utils import nearest_game

def validate_chars(feedcode):
    """Raise an exception if we contain unapproved characters."""
    for c in feedcode:
        if c not in settings.VALID_CHARS:
            raise ValidationError(u"{} is not a valid character.".format(c))

def ensure_unregistered(uname):
    """Ensure the given User has not already registered for this Game."""
    if models.Player.objects.filter(user__username=uname, game=nearest_game()).exists():
        raise ValidationError(u"{} has already registered for this Game.".format(uname))

class TimeValidator:
    def __init__(self, game=None):
        if game is None:
            game = nearest_game()

        self.game = game

    def __call__(self, time):
        """Ensures that the given time is between our start date and now."""
        if time > datetime.now():
            raise ValidationError(u"{} must be in the past.".format(time))

        if time.date() < self.game.start_date:
            raise ValidationError(
                u"The {} game started on {}. This date is {}.".format(
                self.game,
                self.game.start_date,
                time.date()))

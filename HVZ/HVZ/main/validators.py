from django.core.exceptions import ValidationError

from utils import current_game

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

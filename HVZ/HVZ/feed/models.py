from django.db import models

from HVZ.main.models import Building, Game, Player
from HVZ.main.validators import TimeValidator

class Meal(models.Model):
    """Models a successful zombie attack."""

    eater = models.ForeignKey(Player, related_name="meal_set")

    eaten = models.ForeignKey(Player, related_name="eaten_set")

    time = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Building, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{}: {} -> {}".format(eater.game, eater, eaten)

    def clean(self):
        if eater.game != eaten.game:
            raise ValidationError(
                "Eater's game is {}, victim's game is {}.".format(
                    eater.game,
                    eaten.game))

        if time:
            TimeValidator(eater.game)(time)

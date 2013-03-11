from django.core.exceptions import ValidationError
from django.db import models

from HVZ.main.models import Player, Building
from HVZ.main import validators


class Meal(models.Model):
    """Models a successful zombie attack."""

    eater = models.ForeignKey(Player, related_name="meal_set")
    eaten = models.ForeignKey(Player, related_name="eaten_set")

    time = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Building, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{}: {} -> {}".format(self.eater.game, self.eater, self.eaten)

    def clean(self):
        if self.eaten.team != "H":
            raise ValidationError("Victim is not a human.")

        if self.eater.game != self.eaten.game:
            raise ValidationError(
                "Eater's game is {}, victim's game is {}.".format(
                    self.eater.game,
                    self.eaten.game))

        if self.time:
            validators.validate_past(self.time)
            validators.DateValidator(self.eater.game)(self.time.date())

        return super(Meal, self).clean()

    def save(self):
        self.eaten.team = "Z"
        self.eaten.save()
        return super(Meal, self).save()

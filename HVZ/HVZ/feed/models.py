from django.db import models

from main.models import Building, Game, Player
# Create your models here.


class Meal(models.Model):
    """Models a successful zombie attack."""

    eater = models.ForeignKey(Player, related_name="meal_set")
    eaten = models.ForeignKey(Player, related_name="eaten_set")

    game = models.ForeignKey(Game)
    time = models.DateTimeField()
    location = models.ForeignKey(Building, null=True, blank=True)

    description = models.TextField(blank=True)

    def __unicode__(self):
        return u"{}: {} -> {}".format()

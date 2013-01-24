from django.db import models

from main.models import Building, Game
# Create your models here.


class Mission(models.Model):
    DAYS = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
    }

    KINDS = {
        "D": "Day",
        "N": "Night",
        "X": "NPC",
        "L": "Legendary",
    }

    STATUS = {
        "N": "Not Over",
        "HF": "Human Full",
        "HP": "Human Partial",
        "D": "Draw",
        "ZP": "Zombie Partial",
        "ZF": "Zombie Full",
    }

    VISIBILITY = {
        "H": "Humans",
        "Z": "Zombies",
        "B": "Both",
        "M": "Mods",
    }

    human_title = models.CharField(max_length=30, blank=True, null=True)
    zombie_title = models.CharField(max_length=30, blank=True, null=True)

    game = models.ForeignKey(Game)

    day = models.CharField(
        max_length=1,
        choices=[(x, DAYS[x]) for x in DAYS],
    )

    kind = models.CharField(
        max_length=1,
        choices=[(x, KINDS[x]) for x in KINDS],
    )

    visibility = models.CharField(
        max_length=2,
        choices=[(x, VISIBILITY[x]) for x in VISIBILITY],
    )

    def __unicode__(self):
        return u"{}: #{} {}/{}".format(
            self.game,
            self.id,
            self.human_title,
            self.zombie_title,
        )


class MissionBuilding(models.Model):
    LOC_TYPE = {
        "S": "Start",
        "D": "Do Something",
        "F": "Find Something",
        "G": "Go Here",
        "E": "Escort Someone Here",
        "C": "Completion",
    }

    VISIBILITY = {
        "H": "Humans",
        "Z": "Zombies",
        "B": "Both",
        "M": "Mods",
    }

    mission = models.ForeignKey(Mission)
    location = models.ForeignKey(Building)

    kind = models.CharField(
        max_length=1,
        choices=[(x, LOC_TYPE[x]) for x in LOC_TYPE],
    )

    visibility = models.CharField(
        max_length=1,
        choices=[(x, VISIBILITY[x]) for x in VISIBILITY],
    )


class Plot(models.Model):
    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
        "B": "Both",
        "N": "Neither",
    }

    title = models.CharField(max_length=30)
    game = models.ForeignKey(Game)
    visibility = models.CharField(
        max_length=1,
        choices=[(x, TEAMS[x]) for x in TEAMS],
    )

    story = models.TextField()
    reveal_time = models.DateTimeField()

    def __unicode_(self):
        return u"{}: {}".format(self.game, self.title)

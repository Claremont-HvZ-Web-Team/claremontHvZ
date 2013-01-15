from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.db import models

# Create your models here.


class School(models.Model):
    """Representation of a campus"""
    name = models.CharField(max_length=7)

    def __unicode__(self):
        return u"{}".format(self.name)


class Building(models.Model):
    """A building on a campus."""

    KINDS = {
        "C": "Academic",
        "T": "Athletics",
        "D": "Dorm",
        "I": "Dining Hall",
        "L": "Landmark",
        "O": "Other",
    }

    name = models.CharField(max_length=100)
    campus = models.ForeignKey(School, blank=True, null=True)
    building_type = models.CharField(
        max_length=1,
        choices=[(x, KINDS[x]) for x in KINDS],
    )

    def __unicode__(self):
        return "{} ({})".format(
            self.name,
            self.campus,
        )

    def get_kind(self):
        try:
            return self.KINDS[self.building_type]
        except KeyError:
            return None


class Player(models.Model):
    """Game-related data about a user"""

    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
    }

    UPGRADES = {}
    FEED_SZ = 6

    user = models.ForeignKey(User)
    cell = PhoneNumberField(blank=True, null=True)

    game = models.ForeignKey(Game)

    school = models.ForeignKey(School)
    dorm = models.ForeignKey(Building)
    grad_year = models.PositiveIntegerField(blank=True, null=True)

    can_oz = models.BooleanField(default=False)
    can_c3 = models.BooleanField(default=False)
    hardcore = models.BooleanField(default=False)

    feed = models.CharField(max_length=FEED_SZ)

    team = models.CharField(
        max_length=1,
        choices=TEAMS.items(),
        default="H",
    )

    upgrade = models.CharField(
        max_length=1,
        choices=UPGRADES.items(),
        blank=True,
        null=True,
    )

    human_pic = models.ImageField()
    zombie_pic = models.ImageField()

    def __unicode__(self):
        return u"Player: {}".format(self.user)


class PlayerSetting(models.Model):
    """A User's settings"""
    player = models.OneToOneField(Player)

    cell_emergency = models.BooleanField()
    cell_send = models.BooleanField()
    cell_mission_announce = models.BooleanField()
    cell_mission_update = models.BooleanField()
    cell_npc_announce = models.BooleanField()
    cell_npc_update = models.BooleanField()

    def __unicode__(self):
        return u"Settings: {}".format(self.player)


class Game(models.Model):
    """Um. A Game."""
    SEMESTERS = {
        "S": "Spring",
        "F": "Fall",
    }

    semester = models.CharField(
        max_length=1,
        choices=[(x, SEMESTERS[x]) for x in SEMESTERS]
    )
    year = models.PositiveIntegerField()
    start_date = models.DateField()

    def __unicode__(self):
        return u"{} {}".format(
            self.SEMESTERS[self.semester],
            self.year,
        )

class Award(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255)


class Achievement(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    award = models.ForeignKey(Award)
    earned_time = models.DateTimeField()


class ModSchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mod = models.ForeignKey(
        Player,
        limit_choices_to={
            'cell__gte': '1',
            'user__is_staff': 'True',
        }
    )

    def __unicode__(self):
        return u"{}: {} until {}".format(
                self.mod.user.first_name,
                self.start_time.strftime("%a %I:%M %p"),
                self.end_time.strftime("%a %I:%M %p"),
        )


class MonolithController(models.Model):
    admin = models.BooleanField(default=False)
    forcefield = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # prevent additional models
        self.id = 1
        super(MonolithController, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Monolith Controller"

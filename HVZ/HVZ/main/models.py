from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.db import models
from django.conf import settings

from validators import validate_chars


class FeedCodeField(models.CharField):
    default_validators = [validate_chars]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = settings.FEED_LEN
        return super(FeedCodeField, self).__init__(*args, **kwargs)

class School(models.Model):
    """Represents a campus"""
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
        choices=KINDS.items(),
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

class Game(models.Model):
    """Um. A Game."""

    start_date = models.DateField()
    active = models.BooleanField(default=False, unique=True)

    def __unicode__(self):
        if self.active:
            s = u"{} {} (active)"
        else:
            s = u"{} {}"
        return s.format(
            self.semester(),
            self.start_date.year,
        )

    def semester(self):
        """Return 'Spring', 'Summer', or 'Fall', based on academic fiat."""
        if 1 <= self.start_date.month < 6:
            return "Spring"
        elif 6 <= self.start_date.month < 9:
            return "Summer"
        else:
            return "Fall"

    def clean(self):
        """Deactivate any older Games when validating."""

        for g in Game.objects.filter(start_date__lt=self.start_date,
                                     active=True):
            g.active = False
            g.save()

        return super(Game, self).clean()

    class Meta:
        get_latest_by = "start_date"

class Player(models.Model):
    """Game-related data about a user"""

    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
    }

    UPGRADES = {}

    user = models.ForeignKey(User)
    cell = PhoneNumberField(blank=True, null=True)

    game = models.ForeignKey(Game)

    school = models.ForeignKey(School)
    dorm = models.ForeignKey(Building)
    grad_year = models.PositiveIntegerField(blank=True, null=True)

    can_oz = models.BooleanField(default=False)
    can_c3 = models.BooleanField(default=False)

    feed = FeedCodeField()

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

    human_pic = models.ImageField(upload_to=settings.HUMAN_PICS)
    zombie_pic = models.ImageField(upload_to=settings.ZOMBIE_PICS)

    def __unicode__(self):
        return u"Player: {}".format(self.user)

    class Meta:
        # A User can only have one Player per Game.
        unique_together = (("user", "game"),)

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
        return super(MonolithController, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Monolith Controller"

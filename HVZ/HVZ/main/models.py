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
    user = models.OneToOneField(User)
    school = models.ForeignKey(School)
    dorm = models.ForeignKey(Building)

    grad_year = models.PositiveIntegerField(blank=True, null=True)

    cell = PhoneNumberField(blank=True, null=True)

    human_pic = models.ImageField()
    zombie_pic = models.ImageField()

    bad_meals = models.PositiveIntegerField(default=0, blank=False)

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


class Registration(models.Model):
    """An instance of a player in a certain game."""
    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
    }

    HIDDEN_UPGRADES = {
        "R": "Rebel Zombie",
    }

    player = models.ForeignKey(Player)
    hardcore = models.BooleanField(default=False)
    feed = models.CharField(max_length=6)

    game = models.ForeignKey(Game)
    team = models.CharField(
        max_length=1,
        choices=[(x, TEAMS[x]) for x in TEAMS],
        default="H",
    )
    can_oz = models.BooleanField(default=False)
    can_c3 = models.BooleanField(default=False)

    upgrade = models.CharField(
        max_length=1,
        choices=[(x, HIDDEN_UPGRADES[x]) for x in HIDDEN_UPGRADES],
        blank=True,
        null=True,
    )

    bonus = models.PositiveIntegerField(default=0, blank=False)

    def __unicode__(self):
        return u"{}: {} {}".format(
            self.game,
            self.player.first_name(),
            self.player.last_name(),
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

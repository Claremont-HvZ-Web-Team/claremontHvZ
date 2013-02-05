from datetime import date

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.db import models
from django.conf import settings

from HVZ.main.validators import validate_chars
from HVZ.main.exceptions import NoActiveGame


class FeedCodeField(models.CharField):
    default_validators = [validate_chars]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = settings.FEED_LEN
        return super(FeedCodeField, self).__init__(*args, **kwargs)

    def clean(self, value, model):
        return super(FeedCodeField, self).clean(value.upper(), model)


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

    @staticmethod
    def dorms():
        """Return all Buildings in which students typically live."""
        return Building.objects.filter(building_type="D")

    def get_kind(self):
        try:
            return Building.KINDS[self.building_type]
        except KeyError:
            return None


class Game(models.Model):
    """Um. A Game."""

    start_date = models.DateField(unique=True)
    end_date = models.DateField(unique=True)

    def __unicode__(self):
        if self.start_date <= date.today() <= self.end_date:
            s = u"{} {} (ongoing)"
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
        # Two date ranges A and B overlap if:
        # (A.start <= B.end) and (A.end >= B.start)
        try:
            self.objects.get(start_date__lte=self.end_date,
                             end_date__gte=self.start_date)
        except Game.DoesNotExist:
            return super(Game, self).clean()

        raise ValidationError("This Game overlaps with another!")

    @staticmethod
    def unfinished_games():
        """Return the set of all games which haven't yet ended."""
        return Game.objects.filter(end_date__gte=date.today())

    @staticmethod
    def game_in_progress():
        """True iff a Game is currently ongoing."""
        return Game.unfinished_games().filter(
            start_date__lte=date.today()).exists()

    @staticmethod
    def nearest_game():
        """Returns the Game currently ongoing or nearest to now."""
        try:
            return Game.unfinished_games().order_by("start_date")[0]
        except IndexError:
            raise NoActiveGame

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

    profile_pic = models.ImageField(upload_to=settings.HUMAN_PICS,
                                    blank=True, null=True)

    def __unicode__(self):
        return u"Player: {}".format(self.user)

    @classmethod
    def current_players(cls):
        """Return all Players in the current Game."""
        return cls.objects.filter(game=Game.nearest_game())

    @classmethod
    def logged_in_player(cls, request):
        """Return the currently logged in Player."""
        return cls.current_players().get(user=request.user)

    @classmethod
    def user_to_player(cls, u):
        """Return the most current Player corresponding to the given User."""
        return cls.objects.get(game=Game.nearest_game(), user=u)

    class Meta:
        # A User can only have one Player per Game, and a feed code
        # can only correspond to one player per game.
        unique_together = (('user', 'game'), ('feed', 'game'))


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

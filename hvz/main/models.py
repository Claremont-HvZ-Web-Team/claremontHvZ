from django.contrib.auth.models import User
from django.db import models, transaction
from django.conf import settings

from hvz.main import validators

class Game(models.Model):
    """Um. A Game."""

    start_date = models.DateField(unique=True)

    def __str__(self):
        if self.start_date <= settings.NOW().date():
            return u"{} (ongoing)".format(self.season())
        else:
            return self.season()

    def season(self):
        return u"{} {}".format(
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

    @classmethod
    def nearest_game(cls):
        return cls.objects.latest()

    class Meta:
        get_latest_by = "start_date"

class School(models.Model):
    """Represents a campus"""
    name = models.CharField(max_length=64)

    def __str__(self):
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

    campus = models.ForeignKey(
        School,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    building_type = models.CharField(
        max_length=1,
        choices=KINDS.items(),
    )

    def __str__(self):
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

class FeedCodeField(models.CharField):
    default_validators = [validators.validate_feedcode_chars]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = settings.FEED_LEN
        return super(FeedCodeField, self).__init__(*args, **kwargs)

    def clean(self, value, model):
        return super(FeedCodeField, self).clean(value.upper(), model)

class Role(models.Model):
    """Something that makes a human or zombie player special"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    """Game-related data about a user"""

    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    can_oz = models.BooleanField(default=False)
    feed = FeedCodeField()

    team = models.CharField(
        max_length=1,
        choices=TEAMS.items(),
        default="H",
    )

    role = models.ForeignKey(
        Role,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    notes = models.TextField(null=True, blank=True)

    school = models.ForeignKey(
        School,
        related_name="player_set",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    dorm = models.ForeignKey(
        Building,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    grad_year = models.PositiveIntegerField(blank=True, null=True)

    brains = models.PositiveIntegerField(default=0)

    def __str__(self):
        return u"Player: {}".format(self.user.get_full_name())

    @classmethod
    def current_players(cls):
        """Return all Players in the current Game."""
        return cls.objects.filter(game=Game.nearest_game())

    @classmethod
    def logged_in_player(cls, request):
        """Return the currently logged in Player."""
        return cls.current_players().get(user=request.user)

    @classmethod
    def user_to_player(cls, u, game=None):
        """Return the most current Player corresponding to the given User.

        Because a User has multiple players, you can specify which
        player to retrieve by passing a Game.

        """
        if u.is_anonymous:
            raise Player.DoesNotExist

        game = game or Game.nearest_game()
        return cls.objects.get(game=game, user=u)

    class Meta:
        # A User can only have one Player per Game, and a feed code
        # can only correspond to one player per game.
        unique_together = (('user', 'game'), ('feed', 'game'))

class Meal(models.Model):
    """Models a successful zombie attack."""

    eater = models.ForeignKey(
        Player,
        related_name="meal_set",
        on_delete=models.CASCADE,
    )
    eaten = models.ForeignKey(
        Player,
        related_name="eaten_set",
        on_delete=models.CASCADE,
    )

    time = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(
        Building,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return u"{}: {} -> {}".format(
            self.eater.game,
            self.eater,
            self.eaten,
        )

    def save(self):
        if not self.time:
            self.time = settings.NOW()

        self.eaten.team = "Z"
        self.eater.brains += 1

        with transaction.atomic():
            self.eaten.save()
            self.eater.save()

        return super(Meal, self).save()

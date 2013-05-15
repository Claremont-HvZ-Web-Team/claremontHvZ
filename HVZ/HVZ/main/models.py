from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_localflavor_us.models import PhoneNumberField
from django.db import models
from django.conf import settings

from HVZ.main.validators import validate_chars


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
        if self.start_date <= settings.NOW().date() <= self.end_date:
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
        overlapping = Game.objects.filter(start_date__lte=self.end_date,
                                          end_date__gte=self.start_date)

        # But one game can overlap with itself.
        if overlapping.exclude(id=self.id).exists():
            raise ValidationError("This Game overlaps with another!")

        return super(Game, self).clean()

    def is_unfinished(self):
        """True iff the game is still going on."""
        return self.end_date > settings.NOW().date()

    @classmethod
    def games(cls, **flags):
        """Return a list of games satisfying the given arguments.

        @started: True iff you want a game that began in the past.

        @finished: True iff you want a game that has not completed
                   yet.

        @ordered: True iff you want the list of games to be ordered by
                  ascending starting date.

        """
        kwargs = {}

        today = settings.NOW().date()
        if 'started' in flags:
            if flags['started']:
                kwargs['start_date__lte'] = today
            else:
                kwargs['start_date__gt'] = today

        if 'finished' in flags:
            if flags['finished']:
                kwargs['end_date__lt'] = today
            else:
                kwargs['end_date__gte'] = today

        qset = cls.objects.filter(**kwargs)

        if flags.get('ordered'):
            return qset.order_by('start_date')

        return qset

    @classmethod
    def imminent_game(cls):
        """Returns the unfinished Game with the most recent starting date."""
        try:
            return cls.games(finished=False, ordered=True)[0]
        except IndexError:
            raise Game.DoesNotExist

    @classmethod
    def nearest_game(cls):
        """Returns the next Game, if one exists. Otherwise returns the last one."""
        try:
            return cls.imminent_game()
        except Game.DoesNotExist:
            return cls.objects.latest()

    class Meta:
        get_latest_by = "start_date"


class Player(models.Model):
    """Game-related data about a user"""

    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
    }

    UPGRADES = {
        'O': "Original Zombie",
        'P': "Pacifist",
        'n': "Noodler",
        'N': "Noodler II",
        'B': "Black Ops",
        'C': "Charger",
        "D": "Double Tap",
        "S": "Screamer",
        "E": "Bone Zombie",
    }

    user = models.ForeignKey(User)
    cell = PhoneNumberField(blank=True, null=True)

    game = models.ForeignKey(Game)

    school = models.ForeignKey(School)
    dorm = models.ForeignKey(Building, limit_choices_to={'building_type': "D"})
    grad_year = models.PositiveIntegerField(blank=True, null=True)

    can_oz = models.BooleanField(default=False)

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
        return cls.objects.filter(game=Game.imminent_game())

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
        if u.is_anonymous():
            raise Player.DoesNotExist

        game = game or Game.nearest_game()
        return cls.objects.get(game=game, user=u)

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

    @classmethod
    def get_current_mod(cls):
        sched = cls.objects.filter(
            start_time__lte=settings.NOW(),
            end_time__gte=settings.NOW(),
        )
        if sched.exists():
            return sched[0].mod
        return None


class MonolithController(models.Model):
    admin = models.BooleanField(default=False)
    forcefield = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # prevent additional models
        self.id = 1
        return super(MonolithController, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Monolith Controller"

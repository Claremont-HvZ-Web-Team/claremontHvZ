from markupfield import fields

from django.db.models import Q
from django.conf import settings
from django.db import models
from django.utils import timezone

from HVZ.main.models import Game
from HVZ.main import validators

class Mission(models.Model):
    """Traps used by the mods to kill good human players."""

    TIMES = {
        'D': "Day",
        'N': "Night",
    }

    VICTORS = {
        'H': "humans",
        'Z': "zombies",
        'B': "both",
    }

    day = models.DateField()

    time = models.CharField(
        max_length=1,
        choices=TIMES.items(),
    )

    victor = models.CharField(
        max_length=1,
        choices=VICTORS.items(),
        blank=True,
    )

    game = models.ForeignKey(Game)

    def __unicode__(self):
        return u"{}: {} {}".format(
            self.game,
            self.day.strftime("%A"),
            self.TIMES[self.time],
        )

    def clean(self):
        validators.DateValidator(self.game)(self.day)
        return super(Mission, self).clean()

    def start_time(self):
        return settings.START_TIMES[self.time]

    def unfinished(self):
        return not self.victor

    def won(self, team):
        return self.victor in ('B', team)

    class Meta:
        unique_together = (('day', 'time'),)
        get_latest_by = "day"


class Plot(models.Model):
    """The aspects of Missions which are visible to players."""

    TEAMS = {
        "H": "Humans",
        "Z": "Zombies",
    }

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    team = models.CharField(
        max_length=1,
        choices=TEAMS.items(),
    )

    before_story = fields.MarkupField(blank=True, null=True)
    victory_story = fields.MarkupField(blank=True, null=True)
    defeat_story = fields.MarkupField(blank=True, null=True)

    visible = models.NullBooleanField()
    reveal_time = models.DateTimeField(blank=True, null=True)

    mission = models.ForeignKey(Mission)

    def __unicode__(self):
        return self.title

    def clean(self):
        # Set a default time to reveal the next mission.
        if not self.reveal_time:
            self.reveal_time = self.mission.start_time()

        return super(Plot, self).clean()

    @classmethod
    def get_visible(cls, game, team):
        """Returns all plots visible to the given team during the given game."""
        return cls.objects.filter(
            Q(visible=True) | Q(visible__isnull=True, reveal_time__lt=timezone.now()),
            team=team,
            mission__game=game,
        )

    def get_story(self, team):
        if self.mission.unfinished():
            return self.before_story
        elif self.mission.won(team):
            return self.victory_story
        else:
            return self.defeat_story

    def is_visible(self):
        if self.visible == None:
            return timezone.now() >= self.reveal_time

        return self.visible

    class Meta:
        unique_together = (('mission', 'team'),)

from django.db import models
from django.conf import settings

from markupfield.fields import MarkupField

from HVZ.main.models import Player, Game

class Thread(models.Model):
    game = models.ForeignKey(Game)
    team = models.CharField(max_length=1, choices=settings.VERBOSE_TEAMS.items())

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.title

    def visible_to_player(self, player):
        if not player:
            return False

        if player.user.is_staff:
            return True

        if player.game != self.game:
            return False

        if not self.game.is_unfinished():
            return True

        if self.team == 'B':
            return True

        return player.team == self.team

    def visible_to_user(self, user):
        if not user:
            return False

        if user.is_staff:
            return True

        try:
            player = Player.user_to_player(user, self.game)
        except Player.DoesNotExist:
            return False

        return self.visible_to_player(player)

    @staticmethod
    def legal_teams(user):
        if not user:
            return False

        if user.is_staff:
            return settings.VERBOSE_TEAMS.items()

        try:
            player = Player.user_to_player(user)
        except Player.DoesNotExist:
            return []

        return (
            (player.team, settings.VERBOSE_TEAMS[player.team]),
            ('B', settings.VERBOSE_TEAMS['B']),
        )

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name="post_set")
    author = models.ForeignKey(Player)

    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)

    body = MarkupField(default_markup_type="markdown", escape_html=True)

    def __unicode__(self):
        return u"{:<30} ({})".format(self.author, self.created)

    class Meta(object):
        get_latest_by = "updated"

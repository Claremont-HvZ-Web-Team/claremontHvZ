from django.contrib.auth import decorators as auth
from django.core.exceptions import PermissionDenied

from hvz.main import models

def team_required(team):
    def wrapped(*args, **kwargs):
        """Raise an exception if the current user is not of the given team."""
        def check_team(u):
            try:
                player = models.Player.user_to_player(u)
            except models.Player.DoesNotExist:
                raise PermissionDenied("You are not registered for this game!")

            if player.team != team:
                team_name = "human" if team == 'H' else "zombie"
                raise PermissionDenied("You must be a {} to view this page.".format(team_name))
            return True

        return auth.user_passes_test(check_team)(*args, **kwargs)
    return wrapped

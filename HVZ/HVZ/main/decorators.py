from functools import wraps

from django.contrib.auth import decorators as auth
from django.core.exceptions import PermissionDenied

from HVZ.main.exceptions import NoActiveGame, NoUnfinishedGames
from HVZ.main.models import Game, Player


def require_active_game(view_func):
    """Raise an exception if no game is in progress."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not Game.games(started=True, finished=False).exists():
            raise NoActiveGame
        return view_func(*args, **kwargs)

    return wrapper


def require_unfinished_game(view_func):
    """Raise an exception if no unfinished games are in progress."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not Game.games(finished=False).exists():
            raise NoUnfinishedGames
        return view_func(*args, **kwargs)

    return wrapper

# Player team checks

def team_required(team):
    def wrapped(*args, **kwargs):
        """Raise an exception if the current user is not of the given team."""
        def check_team(u):
            try:
                player = Player.user_to_player(u)
            except Player.DoesNotExist:
                raise PermissionDenied("You are not registered for this game!")

            if player.team != team:
                team_name = "human" if team == 'H' else "zombie"
                raise PermissionDenied("You must be a {} to view this page.".format(team_name))
            return True

        return auth.user_passes_test(check_team)(*args, **kwargs)
    return wrapped

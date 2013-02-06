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


def zombie_required(*args, **kwargs):
    """Raise an exception if the current user is not a zombie."""
    def check_zombie(u):
        try:
            player = Player.user_to_player(u)
        except Player.DoesNotExist:
            raise PermissionDenied("You are not registered for this game!")

        if player.team != "Z":
            raise PermissionDenied("You must be a zombie to view this page.")
        return True

    return auth.user_passes_test(check_zombie)(*args, **kwargs)


def human_required(*args, **kwargs):
    def check_human(u):
        if Player.user_to_player(u).team != "H":
            raise PermissionDenied("You must be a human to view this page.")
        return True

    return auth.user_passes_test(check_human)(*args, **kwargs)

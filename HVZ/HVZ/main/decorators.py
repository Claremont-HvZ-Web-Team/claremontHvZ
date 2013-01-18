from functools import wraps

from django.core.urlresolvers import reverse
from django.contrib.auth import decorators as auth

from HVZ.main.exceptions import NoActiveGame, NoUnfinishedGames
from HVZ.main import utils

def require_active_game(view_func):
    """Raise an exception if no game is in progress."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not utils.game_in_progress():
            raise NoActiveGame
        return view_func(*args, **kwargs)

    return wrapper

def require_unfinished_game(view_func):
    """Raise an exception if no unfinished games are in progress."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not utils.unfinished_games().exists():
            raise NoUnfinishedGames
        return view_func(*args, **kwargs)

    return wrapper

# Player team checks

def zombie_required(*args, **kwargs):
    """Raise an exception if the current user is not a zombie."""
    def check_zombie(u):
        if user_to_player(u).team != "Z":
            raise WrongTeamException
        return True

    return auth.user_passes_test(check_zombie)(*args, **kwargs)

def human_required(*args, **kwargs):
    def check_human(u):
        if user_to_player(u).team != "H":
            raise WrongTeamException
        return True

    return auth.user_passes_test(check_human)(*args, **kwargs)

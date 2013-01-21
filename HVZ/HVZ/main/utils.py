from datetime import date

import models
from exceptions import NoActiveGame

# Game retrieval functions.

def unfinished_games():
    """Return the set of all games which haven't yet ended."""
    return models.Game.objects.filter(end_date__gte=date.today())

def game_in_progress():
    """True iff a Game is currently ongoing."""
    return unfinished_games().filter(start_date__lte=date.today()).exists()

def nearest_game():
    """Returns the Game currently ongoing or nearest to now."""
    try:
        return unfinished_games().order_by("start_date")[0]
    except IndexError:
        raise NoActiveGame

# Player retrieval functions.

def current_players():
    """Return all Players in the current Game."""
    return models.Player.objects.filter(game=nearest_game())

def logged_in_player(request):
    """Return the currently logged in Player."""
    return models.current_players().get(user=request.user)

def user_to_player(u):
    """Return the most current Player corresponding to the given User."""
    return models.Player.objects.filter(game=nearest_game(), user=u).get()

# Building retrieval functions.

def dorms():
    """Return all Buildings in which students typically live."""
    return models.Building.objects.filter(building_type="D")

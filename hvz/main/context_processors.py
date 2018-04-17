from django.conf import settings

from hvz.main import models


def inject_outbreak_percentage(request):
    try:
        newest_game = models.Game.nearest_game()
    except models.Game.DoesNotExist:
        # Just return an arbitrary sane value
        return {'outbreak_percent': 96}

    players = models.Player.objects.filter(game=newest_game)
    humans = players.filter(team='H')

    nPlayers = players.count()

    if nPlayers > 0:
        percent = humans.count() * 100. / nPlayers
    else:
        percent = 100

    return {'outbreak_percent': min(96, percent)}


def inject_current_player(request):
    try:
        player = models.Player.user_to_player(request.user)
    except (models.Player.DoesNotExist, models.Game.DoesNotExist):
        player = None
    return {'player': player}

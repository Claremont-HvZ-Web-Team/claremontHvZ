from HVZ.main.models import Player, Game


def inject_outbreak_percentage(request):
    try:
        latest_game = Game.games(started=True).latest()
    except Game.DoesNotExist:
        # Just return an arbitrary sane value
        return {'outbreak_percent': 96}

    players = Player.objects.filter(game=latest_game)
    humans = players.filter(team='H')

    nPlayers = players.count()

    if nPlayers > 0:
        percent = humans.count() * 100. / nPlayers
    else:
        percent = 100

    return {'outbreak_percent': min(96, percent)}

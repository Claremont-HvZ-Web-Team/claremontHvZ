from django.conf import settings

from HVZ.main.models import Player, Game, ModSchedule


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


def inject_current_player(request):
    try:
        player = Player.user_to_player(request.user)
    except (Player.DoesNotExist, Game.DoesNotExist):
        player = None
    return {'player': player}


def inject_mod_info(request):
    print ModSchedule.get_current_mod()
    return {
        'CURRENT_MOD': ModSchedule.get_current_mod(),
        'MOD_PHONE_NUMBER': settings.MOD_PHONE_NUMBER,
    }

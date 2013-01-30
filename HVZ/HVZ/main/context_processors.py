from HVZ.main.models import Player


def inject_outbreak_percentage(request):
    humans = Player.objects.filter(team='H').count()
    print "humans", humans
    players = Player.objects.count()
    print "players", players
    percent = (float(humans) / players) * 100 if players > 0 else 0
    print "percent", percent
    return {'outbreak_percent': min(96, percent)}

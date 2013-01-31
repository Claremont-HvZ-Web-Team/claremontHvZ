from HVZ.main.models import Player


def inject_outbreak_percentage(request):
    humans = Player.objects.filter(team='H').count()
    players = Player.objects.count()
    percent = (float(humans) / players) * 100 if players > 0 else 0
    return {'outbreak_percent': min(96, percent)}

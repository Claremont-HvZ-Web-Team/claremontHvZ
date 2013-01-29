from HVZ.main.models import Player


def inject_outbreak_percentage(request):
    zombies = Player.objects.filter(team='Z').count()
    players = Player.objects.count()
    percent = (float(zombies) / players) * 100 if players > 0 else 0
    return {'outbreak_percent': min(96, percent)}

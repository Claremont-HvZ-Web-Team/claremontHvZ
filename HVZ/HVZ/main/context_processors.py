from HVZ.main.models import Player


def inject_outbreak_percentage(request):
    zombies = Player.objects.filter(team='Z').count()
    percent = (float(zombies) / Player.objects.count()) * 100
    return {'outbreak_percent': min(96, percent)}

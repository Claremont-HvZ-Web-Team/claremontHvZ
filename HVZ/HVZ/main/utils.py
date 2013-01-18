import models

def current_game():
    return models.Game.objects.filter(active=True).get()

def current_players():
    return models.Player.objects.filter(game=current_game())

def logged_in_player(request):
    return current_players().get(user=request.user)

def dorms():
    return models.Building.objects.filter(building_type="D")

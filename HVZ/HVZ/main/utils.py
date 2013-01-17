from models import Game, Player

def current_game():
    return Game.objects.latest()

def current_players():
    return Player.objects.filter(game=current_game())

def logged_in_player(request):
    return current_players().get(user=request.user)

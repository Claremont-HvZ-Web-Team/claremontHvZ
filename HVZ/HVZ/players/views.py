from django.db.models import Count
from django.views.generic.list import ListView

from HVZ.main.models import Player, Game


class PlayerListView(ListView):
    model = Player
    template_name = 'players/player_list.html'

    def get_queryset(self):
        game = Game.nearest_game()
        return (Player.objects.filter(game=game).
                select_related('user').
                annotate(meal_count=Count('meal_set')))


class PlayerEmailView(ListView):
    model = Player
    template_name = 'players/email_list.html'

    def get_queryset(self):
        game = Game.nearest_game()
        return Player.objects.filter(game=game)

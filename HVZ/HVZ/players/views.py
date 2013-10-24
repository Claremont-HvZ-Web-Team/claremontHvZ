from django.db.models import Count
from django.views.generic.list import ListView

from HVZ.main.models import Player, Game, School


class PlayerListView(ListView):
    model = Player
    template_name = 'players/player_list.html'

    def get(self, request, *args, **kwargs):
        self.kwargs['school'] = request.GET.get('school', '')
        self.kwargs['gradyear'] = request.GET.get('gradyear', '')
        return super(PlayerListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        players = kwargs.get('object_list')

        context = super(PlayerListView, self).get_context_data(**kwargs)
        context['game_season'] = Game.nearest_game().season()

        context['schools'] = School.objects.all().annotate(
            num_players=Count('player_set')
        ).order_by('-num_players')

        context['years'] = map(str, sorted(set([p.grad_year for p in Player.current_players()])))
        context['school'] = self.kwargs.get('school', '')
        context['gradyear'] = self.kwargs.get('gradyear', '')

        return context

    def get_queryset(self):
        queryset = Player.current_players()

        if self.kwargs.get('gradyear'):
            queryset = queryset.filter(grad_year=self.kwargs['gradyear'])

        if self.kwargs.get('school'):
            queryset = queryset.filter(school__name__istartswith=self.kwargs['school'])

        return (queryset.
                select_related('user', 'school__name').
                annotate(meal_count=Count('meal_set')).
                order_by('-meal_count'))


class PlayerEmailView(ListView):
    model = Player
    template_name = 'players/email_list.html'

    def get_queryset(self):
        game = Game.nearest_game()
        return Player.objects.filter(game=game)

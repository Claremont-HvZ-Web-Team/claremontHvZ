from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

from HVZ.main.models import Game
from HVZ.main.mixins import PlayerAwareMixin
from HVZ.main.decorators import require_active_game
from HVZ.missions.models import Plot

class PlotListView(ListView, PlayerAwareMixin):
    """Show a list of missions to the player."""

    @method_decorator(login_required)
    @method_decorator(require_active_game)
    def dispatch(self, request, *args, **kwargs):
        super(PlotListView, self).set_player(request)
        return super(PlotListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        game = Game.imminent_game()
        team = self.player.team
        return Plot.objects.filter(
            mission__game=game,
            team=team,
        ).order_by('-reveal_time').select_related('mission')

    def get_context_data(self, **kwargs):
        context = super(PlotListView, self).get_context_data(**kwargs)
        context['player'] = self.player
        return context

class PlotDetailView(DetailView, PlayerAwareMixin):
    """Show a particular mission to the player."""
    model = Plot

    def dispatch(self, request, *args, **kwargs):
        super(PlotDetailView, self).set_player(request)
        return super(PlotDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlotDetailView, self).get_context_data(**kwargs)
        context['story'] = context['plot'].get_story(self.player.team)
        return context

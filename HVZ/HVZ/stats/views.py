import calendar
from datetime import datetime, time, timedelta
from collections import defaultdict

from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView, ListView
from django.conf import settings

from HVZ.main.models import Building, Game, Player, School
from HVZ.main.mixins import JSONResponseMixin
from HVZ.feed.models import Meal


class PopStatPage(TemplateView):
    template_name = 'stats/pop_stats.html'


class MealLog(ListView):
    template_name = 'stats/meal_log.html'

    def get_queryset(self, *args, **kwargs):
        return (Meal.objects.filter(eater__game=Game.nearest_game())
                .select_related(
                    'eater__user__first_name', 'eater__user__last_name',
                    'eaten__user__first_name', 'eaten__user__last_name',
                ).order_by('time'))


class AncestryPage(TemplateView):
    template_name = 'stats/ancestry.html'


class OutbreakPage(TemplateView):
    template_name = 'stats/outbreak.html'

def json_format_time(datetime_object):
    """Convert a Python datetime object to a JS timestamp"""
    # We really need to store our times in UTC. Until then, we can at
    # least understand our mistakes.
    if timezone.is_naive(datetime_object):
        datetime_object = timezone.make_aware(datetime_object, timezone.get_default_timezone())

    return calendar.timegm(datetime_object.utctimetuple()) * 1000


class JSONPopulationTimeSeries(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        return Meal.objects.filter(eater__game=Game.nearest_game(), time__isnull=False)

    def raw_serialization(self, context):
        game = Game.nearest_game()

        t0, tf = time_endpoints(game)

        players = Player.current_players().all()
        meals = Meal.objects.select_related('eaten').all()
        eaten_zombies = set([m.eaten for m in meals])
        ozs = [p for p in players if p.team == 'Z' and p not in eaten_zombies]

        num_zombies = len(ozs)
        num_humans = len(players) - num_zombies

        human_tally = []
        zombie_tally = []

        meals_vs_hours = meals_per_hour(game, self.get_queryset())
        for hour in xrange(len(meals_vs_hours)):
            t = t0 + timedelta(hours=hour)

            # Stop the graph at the current time
            if t > settings.NOW():
                break

            meal_count = meals_vs_hours[hour]

            num_humans -= meal_count
            num_zombies += meal_count

            human_tally.append([json_format_time(t), num_humans])
            zombie_tally.append([json_format_time(t), num_zombies])

        if not human_tally:
            human_tally = [[json_format_time(t0), num_humans]]

        if not zombie_tally:
            zombie_tally = [[json_format_time(t0), num_zombies]]

        return [
            {'label': 'humans', 'data': human_tally, 'color': 'rgb(128, 0, 0)'},
            {'label': 'zombies', 'data': zombie_tally, 'color': 'rgb(0, 128, 0)'},
        ]


def time_endpoints(game):
    """Return the start and end times of the game.

    Assume we start at 8am and finish at 11pm.

    """
    t0 = datetime.combine(game.start_date, time(hour=8))
    tf = datetime.combine(game.end_date, time(hour=23))

    return t0, tf

class JSONTagHistogram(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        return Meal.objects.filter(eater__game=Game.nearest_game(), time__isnull=False)

    def raw_serialization(self, context):
        game = Game.nearest_game()
        t0, tf = time_endpoints(game)

        meals_vs_hours = meals_per_hour(Game.nearest_game(), self.get_queryset())

        histogram = []
        for hour in xrange(len(meals_vs_hours)):
            t = t0 + timedelta(hours=hour)

            # Stop at the current time
            if t > settings.NOW():
                break

            histogram.append([json_format_time(t), meals_vs_hours[hour]])

        # Pre-game case
        if not histogram:
            histogram = [[json_format_time(t0), 0]]

        return [{
            "data": histogram,
            "color": "rgb(0, 128, 0)",
        }]

def meals_per_hour(game, meals):
    """Return the number of meals in each hour between now and the game's end."""
    # If we got a queryset, evaluate it now.
    meals = list(meals)

    t0, tf = time_endpoints(game)

    meals_vs_hours = defaultdict(int)
    for m in meals:
        num_hours = hours_between(m.time, t0)
        meals_vs_hours[num_hours] += 1

    num_hours = hours_between(tf, t0)
    aggregates = []
    for hour in xrange(num_hours):
        aggregates.append(meals_vs_hours[hour])

    return aggregates


def hours_between(t1, t2):
    dt = abs(t2 - t1)
    return dt.days*24 + dt.seconds/3600


class JSONZombieAncestry(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        return None

    def raw_serialization(self, context):
        self.players = Player.current_players().filter(team='Z').select_related('user')
        self.names = {p: p.user.get_full_name() for p in self.players}
        self.meals = (Meal.objects.filter(eater__game=Game.nearest_game())
                      .select_related('eater', 'eaten'))

        self.possible_ozs = set(self.players)
        self.children = defaultdict(list)
        for m in self.meals:
            if m.eaten not in self.players:
                continue
            self.children[m.eater].append(m.eaten)
            self.possible_ozs.remove(m.eaten)

        ozs = [p for p in self.players if p in self.possible_ozs]

        return {
            "name": "Subject Zero",
            "children": map(self.traverse, ozs),
        }

    def traverse(self, zombie):
        """Return a nested tree of the given zombie and all its children"""
        children = self.children[zombie]

        return {
            "name": self.names[zombie],
            "children": [self.traverse(c) for c in children] if children else None,
        }


class JSONPlayerStats(JSONResponseMixin, BaseListView):
    FIELDS = ('team', 'grad_year', 'school', 'dorm')

    @staticmethod
    def _bounded_grad_year(grad_year):
        return abs(Game.nearest_game().start_date.year - grad_year) < 5

    def get_queryset(self):
        return Player.current_players()

    def raw_serialization(self, context):
        actual = super(JSONPlayerStats, self).raw_serialization(context)

        aggregates = {
            'grad_year': [
                {'label': 'zombies', 'data': defaultdict(int), 'color': 'rgb(0, 128, 0)'},
                {'label': 'humans', 'data': defaultdict(int), 'color': 'rgb(128,0,0)'},
            ],
            'dorm': [
                {'label': 'zombies', 'data': defaultdict(int), 'color': 'rgb(0, 128, 0)'},
                {'label': 'humans', 'data': defaultdict(int), 'color': 'rgb(128,0,0)'},
            ],
            'school': [
                {'label': 'zombies', 'data': defaultdict(int), 'color': 'rgb(0, 128, 0)'},
                {'label': 'humans', 'data': defaultdict(int), 'color': 'rgb(128,0,0)'},
            ],
        }

        dorms = Building.objects.filter(building_type="D").order_by("name").values('id', 'name')
        dorm_ordering = list(b['id'] for b in dorms)
        dorm_name_ordering = list(b['name'] for b in dorms)
        axis_lookup = {
            'grad_year': {},  # 2013, etc.
            'dorm': dict(enumerate(dorm_name_ordering)),  # 0: Atwood Dorm, etc.
            'school': {d['id']: d['name'] for d in School.objects.order_by('name').values('id', 'name')},
        }


        for item in actual:
            index = 0 if item['team'] == "Z" else 1

            if item['grad_year']:

                axis_lookup['grad_year'].setdefault(item['grad_year'], str(item['grad_year']))

            for key in aggregates:
                if item[key]:
                    try:
                        if key == 'grad_year' and not self._bounded_grad_year(item['grad_year']):
                            continue

                        if key == 'dorm':
                            aggregates[key][index]['data'][dorm_ordering.index(item[key])] += 1
                        else:
                            aggregates[key][index]['data'][item[key]] += 1
                    except KeyError:
                        continue

        aggregates['ticks'] = axis_lookup
        # convert all data dicts to arrays
        for key in aggregates:
            if key == "ticks":
                for tick_set in aggregates[key]:
                    aggregates[key][tick_set] = [[int(_id), val] for _id, val in aggregates[key][tick_set].items()]
                continue
            for data_set in aggregates[key]:
                if key == 'dorm':
                    # flip dorm data series for horizontal bars
                    data_set['data'] = [[val, dkey] for dkey, val in data_set['data'].items()]
                    data_set['data'].sort(cmp=(lambda x, y: x[1] - y[1]))
                else:
                    data_set['data'] = [[dkey, val] for dkey, val in data_set['data'].items()]

        return aggregates

from datetime import datetime, time, timedelta
from collections import defaultdict

from django import http
from django.core import serializers
import django.utils.simplejson as json
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView, ListView
from django.conf import settings

from HVZ.main.models import Building, Game, Player, School
from HVZ.feed.models import Meal


class PopStatPage(TemplateView):
    template_name = 'stats/pop_stats.html'


class MealLog(ListView):
    template_name = 'stats/meal_log.html'

    def get_queryset(self, *args, **kwargs):
        return Meal.objects.filter(eater__game=Game.nearest_game()).select_related(
                       'eater__user__first_name', 'eater__user__last_name',
                       'eaten__user__first_name', 'eaten__user__last_name',
            'argabarga').order_by('time')


class AncestryPage(TemplateView):
    template_name = 'stats/ancestry.html'


class OutbreakPage(TemplateView):
    template_name = 'stats/outbreak.html'


class JSONResponseMixin(object):
    SERIALIZER = serializers
    FIELD_NAME = 'object_list'
    FIELDS = ()

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json;charset=UTF-8',
                                 **httpresponse_kwargs)

    def raw_serialization(self, context):
        raw_data = self.SERIALIZER.serialize(
            'python',
            context[self.FIELD_NAME],
            fields=self.FIELDS,
        )

        return [d['fields'] for d in raw_data]

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.

        return json.dumps(self.raw_serialization(context))


class JSONPopulationTimeSeries(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        return Meal.objects.filter(eater__game=Game.nearest_game())

    def raw_serialization(self, context):
        game = Game.nearest_game()

        t0, tf = time_endpoints(game)

        num_zombies = Player.current_players().filter(upgrade='O').count()
        num_humans = Player.current_players().count() - num_zombies

        human_tally = []
        zombie_tally = []

        meals_vs_hours = meals_per_hour(game, self.get_queryset())
        for hour in xrange(len(meals_vs_hours)):
            if t0 + timedelta(hours=hour) > settings.NOW():
                continue

            meal_count = meals_vs_hours[hour]

            num_humans -= meal_count
            num_zombies += meal_count

            human_tally.append([hour, num_humans])
            zombie_tally.append([hour, num_zombies])

        if not human_tally:
            human_tally = [[0, num_humans]]

        if not zombie_tally:
            zombie_tally = [[0, num_zombies]]

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

class JSONOutbreak(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        return Meal.objects.filter(eater__game=Game.nearest_game())

    def raw_serialization(self, context):
        return meals_per_hour(Game.nearest_game(), self.get_queryset())


def meals_per_hour(game, meals):
    """Return the number of meals in each hour between now and the game's end."""
    # If we got a queryset, evaluate it now.
    meals = list(meals)

    t0, tf = time_endpoints(game)
    dt = timedelta(hours=1)

    meals_vs_hours = defaultdict(int)
    for m in meals:
        num_hours = hours_between(m.time, t0)
        meals_vs_hours[num_hours] += 1

    num_hours = hours_between(tf, t0)
    aggregates = []
    for hour in xrange(num_hours):
        aggregates.append(meals_vs_hours[hour])

    if settings.DEBUG:
        assert(sum(aggregates) == len(meals))

    return aggregates


def hours_between(t1, t2):
    dt = abs(t2 - t1)
    return dt.days*24 + dt.seconds/3600


class JSONZombieAncestry(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        return None

    def raw_serialization(self, context):
        self.players = Player.current_players().select_related('user')
        self.names = {p: p.user.get_full_name() for p in self.players}
        self.meals = (Meal.objects.filter(eater__game=Game.nearest_game())
                      .select_related('eater', 'eaten'))

        self.children = defaultdict(list)
        for m in self.meals:
            self.children[m.eater].append(m.eaten)

        ozs = [p for p in self.players if p.upgrade == 'O']

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
                else:
                    data_set['data'] = [[dkey, val] for dkey, val in data_set['data'].items()]
        return aggregates

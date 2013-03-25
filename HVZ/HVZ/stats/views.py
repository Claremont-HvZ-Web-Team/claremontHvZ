from collections import defaultdict

from django import http
from django.core import serializers
import django.utils.simplejson as json
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView

from HVZ.main.models import Building, Game, Player, School


class FullStatPage(TemplateView):
    template_name = 'stats/the_stats.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FullStatPage, self).get_context_data(*args, **kwargs)

        return context


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
                                 content_type='application/json',
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


class JSONPlayerStats(JSONResponseMixin, BaseListView):
    FIELDS = ('team', 'grad_year', 'school', 'dorm')
    # def get_context_data(self, *args, **kwargs):
    #     context = super(JSONPlayerStats, self).get_context_data(*args, **kwargs)

    #     context['objects'] = Player.objects.all().filter(game=Game.imminent_game()).values(
    #         'team',
    #         'grad_year',
    #         'school',
    #         'dorm',
    #     )

    #     return context
    def get_queryset(self):
        return Player.objects.all().filter(game=Game.imminent_game())

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

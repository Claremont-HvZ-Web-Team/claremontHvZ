from django import http
from django.core import serializers
import django.utils.simplejson as json
from django.views.generic import TemplateView, View
from django.views.generic.list import BaseListView

from HVZ.main.models import Player, Game


class FullStatPage(TemplateView):
    template_name = 'stats/the_stats.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FullStatPage, self).get_context_data(*args, **kwargs)

        return context


class JSONResponseMixin(object):
    SERIALIZER = serializers
    FIELD_NAME = 'object_list'

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return self.SERIALIZER.serialize('json', context[self.FIELD_NAME],
            fields=('team', 'grad_year', 'school', 'dorm'),
        )


class JSONPlayerStats(JSONResponseMixin, BaseListView):

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

    def convert_context_to_json(self, context):

        players = context[self.FIELD_NAME]



        return super(JSONPlayerStats, self).convert_context_to_json(context)

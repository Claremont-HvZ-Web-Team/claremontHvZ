import json

from django import http
from django.core import serializers
from django.core.exceptions import PermissionDenied

from HVZ.main.models import Player, Game


class CurrentGameMixin(object):
    """Passes the current game to the view."""

    _game = None

    @property
    def game(self):
        if self._game:
            return self._game
        try:
            self._game = Game.nearest_game()
        except Game.DoesNotExist:
            raise PermissionDenied("You need to create a game!")

        return self._game


class PlayerAwareMixin(object):
    """Passes the current player to the view."""

    _player = None

    @property
    def player(self):
        if self._player:
            return self._player
        try:
            self._player = Player.user_to_player(self.request.user, self.game)
        except Player.DoesNotExist:
            raise PermissionDenied("You are not registered for this game!")

        return self._player


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

import json

from django.core import serializers
from django import http

def json_response(content, **httpresponse_kwargs):
    return http.HttpResponse(
        json.dumps(content),
        content_type='application/json;charset=UTF-8',
        **httpresponse_kwargs,
    )

class JSONResponseMixin(object):
    SERIALIZER = serializers
    FIELD_NAME = 'object_list'
    FIELDS = ()

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return get_json_response(self.convert_context_to_json(context))

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

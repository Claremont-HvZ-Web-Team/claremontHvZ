# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

class HttpResponseJson(HttpResponse):
    def __init__(self, data):
        json_data = simplejson.dumps(data)
        super(HttpResponseJson, self).__init__(
            content=json_data, mimetype='application/json')


def backurl(request, default='/'):
    """
    Return previous url from user's browser history using Referer
    header or ``default`` as fallback value.
    """

    return request.META.get('HTTP_REFERER', None) or default

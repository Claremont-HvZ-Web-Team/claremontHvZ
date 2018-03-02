# -*- coding: utf-8 -*-
"""
Contains view's decorators which automates common tasks.
"""

import traceback

from django.shortcuts import render_to_response
from django.template import RequestContext

from common.http import HttpResponseJson

def render_to(template):
    """
    Render view's output with ``template`` using ``RequestContext``.

    If decorated view returns dict object then wrap it in RequestContext and
    render the template.

    If decorated view returns non dict object then just return this object.

    Args:
        :template: path to template
    
    Example::

        @render_to('blog/index.html')
        def post_list(request):
            posts = Post.objects.all()
            return {'posts': posts,
                    }
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            else:
                ctx = RequestContext(request)
                return render_to_response(template, output, context_instance=ctx)
        return wrapper
    return decorator


def ajax(func):
    """
    Convert views's output into JSON.

    Decorated view should return dict object.

    If ``request.method`` is not ``POST`` then deny the request.

    If view raises Exception then return JSON message with error description.
    """

    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                response = func(request, *args, **kwargs)
            except Exception, ex:
                response = {'error': traceback.format_exc()}
        else:
            response = {'error': {'type': 403, 'message': 'Accepts only POST request'}}
        if isinstance(response, dict):
            return HttpResponseJson(response)
        else:
            return response
    return wrapper


def ajax_get(func):
    """
    Convert views's output into JSON.

    Decorated view should return dict object.

    If view raises Exception then return JSON message with error description.
    """

    def wrapper(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
        except Exception, ex:
            response = {'error': traceback.format_exc()}
        if isinstance(response, dict):
            return HttpResponseJson(response)
        else:
            return response
    return wrapper


def disable_cache(func):
    def decorated(*args, **kwargs):
        resp = func(*args, **kwargs)
        resp['Pragma'] = 'no-cache'
        resp['Expires'] = '0'
        resp['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp
    return decorated

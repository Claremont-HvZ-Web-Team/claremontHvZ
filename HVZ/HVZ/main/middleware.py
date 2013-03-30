from django.core.exceptions import PermissionDenied
from django.template import RequestContext, loader
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings


class Http403Middleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return render(request,
                          "403.html", 
                          dictionary={"message": unicode(exception)},
                          status=403,
                   )

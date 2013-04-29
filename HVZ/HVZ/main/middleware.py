from django.core.exceptions import PermissionDenied
from django.shortcuts import render


class Http403Middleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return render(request,
                          "403.html", 
                          dictionary={"message": unicode(exception)},
                          status=403,
                   )

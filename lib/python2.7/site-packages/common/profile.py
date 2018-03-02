"""
This middleware based on http://code.google.com/p/django-profiling/source/browse/trunk/profiling/middleware.py"""

import sys
import tempfile
import hotshot
import hotshot.stats
from cStringIO import StringIO
try:
    from guppy import hpy
    guppy_installed = True
except ImportError:
    guppy_installed = False

from django.conf import settings
from django.http import HttpResponse

class ProfileMiddleware(object):
    """
    Displays hotshot profiling for any view.
    http://yoursite.com/yourview/?prof

    Add the "prof" key to query string by appending ?prof (or &prof=)
    and you'll see the profiling results in your browser.
    It's set up to only be available in django's debug mode,
    but you really shouldn't add this middleware to any production configuration.
    * Only tested on Linux
    """
    def process_request(self, request):
        if 'prof' in request.GET:
            self.tmpfile = tempfile.NamedTemporaryFile()
            self.prof = hotshot.Profile(self.tmpfile.name)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if 'prof' in request.GET:
            return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)

    def process_response(self, request, response):          
        if 'prof' in request.GET:
            if guppy_installed:
                h = hpy()
                mem_profile = h.heap()
            else:
                mem_profile = 'guppy package is not installed'
            
            self.prof.close()

            out = StringIO()
            old_stdout = sys.stdout
            sys.stdout = out

            stats = hotshot.stats.load(self.tmpfile.name)
            #stats.strip_dirs()
            stats.sort_stats('cumulative')
            stats.print_stats()

            sys.stdout = old_stdout
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                out = response.content.split('</body>')
                tail = """
                    <div style="text-align: left">
                        <h1>Instance wide RAM usage</h1>
                        <pre>%s</pre>
                        <br/><br/><br/>
                        <h1>CPU Time for this request</h1>
                        <pre>%s</pre>
                    </div>
                """ % (mem_profile, stats_str)
                out = out[0] + tail + out[1]
                return HttpResponse(out)
                    
        return response

#
# Copyright (c) 2011 Thomas Rampelberg
#

"""Making cross-domain requests easy on the server (for GAE).

See the readme at https://github.com/pyronicide/janky.post for more details.
"""

__author__ = 'Thomas Rampelberg'
__author_email__ = 'thomas@saunter.org'

from google.appengine.ext import webapp
import json
import logging
import urlparse

class JankyMiddleware(object):
    """WSGI middleware that adds janky support."""

    tmpl = """<html><head></head><body>
<script type="text/javascript">
  window.name = %(resp)s;
  location.href = %(origin)s;
</script>
</body></html>
"""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def my_start_response(status, headers, exc_info=None):
            write = start_response(status, headers, exc_info)
            def my_write(body):
                if not body: return
                origin = webapp.Request(environ).get('_origin')
                if origin:
                    body = self.tmpl % { 
                        'resp': json.dumps(body), 
                        'origin': json.dumps(urlparse.urljoin(
                                webapp.Request(environ).get('_origin'), 
                                '/janky'))
                        }
                write(body)
            return my_write
        return self.app(environ, my_start_response)

"""
main:
    component: notfound
"""

from wiseguy import WSGIComponent

class NotFoundFactory(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, environ, start_response):
        from webob.exc import HTTPNotFound
        r = HTTPNotFound()
        return r(environ, start_response)

NotFoundComponent = WSGIComponent(
    schema = None,
    factory = NotFoundFactory,
    )

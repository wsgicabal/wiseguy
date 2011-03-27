"""
main:
    component: helloworld
"""

from wiseguy import WSGIComponent

class HelloWorldFactory(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, environ, start_response):
        from webob import Response
        r = Response()
        r.body = '<html><body><h1>Hello world!</h1></body></html>'
        return r(environ, start_response)

HelloWorldComponent = WSGIComponent(
    schema = None,
    factory = HelloWorldFactory,
    )

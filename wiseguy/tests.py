import colander
from webob import Response

class DummySchema(colander.MappingSchema):
    foo = colander.SchemaNode(colander.Int())

class DummyFactory(object):

    def __init__(self, **kwargs):
        print 'DummyFactory called with %r' % kwargs

    def __call__(self, environ, start_response):
        r = Response()
        r.body = '<h1>Hello dummy</h1>'
        return r(environ, start_response)

class DummyFilterFactory(object):

    def __init__(self, app, **kwargs):
        print 'DummyFilterFactory called with %r, %r' % (app, kwargs)
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

class DummyApp(object):
    pass

class DummyComponent(object):
    schema = DummySchema()
    factory = DummyFactory

class DummyFilter(object):
    schema = colander.MappingSchema()
    factory = DummyFilterFactory

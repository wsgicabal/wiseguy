import unittest

class TestAppLoaderFunctional(unittest.TestCase):
    def test_it(self):
        from StringIO import StringIO
        import webob
        import gzip
        import paste.gzipper
        from wiseguy.loader import AppLoader
        loader = AppLoader()
        loader.add_component('dummyfilter', DummyFilter)
        loader.add_component('dummycomponent', DummyComponent)
        loader.load_yaml(test_config_file)
        app_factory = loader.get_app_factory('main')
        app = app_factory()
        self.assertEqual(app.__class__, paste.gzipper.middleware)
        self.assertEqual(app.application.__class__, DummyFilterFactory)
        self.assertEqual(app.application.app.__class__, DummyFactory)
        request = webob.Request.blank('/')
        request.environ['HTTP_ACCEPT_ENCODING'] = 'gzip'
        status, headerlist, body = request.call_application(app)
        self.assertEqual(status, '200 OK')
        self.assertEqual(headerlist,
                         [('Content-Type', 'text/html; charset=UTF-8'),
                          ('content-encoding', 'gzip'),
                          ('Content-Length', '38')])
        io = StringIO(body[0])
        f = gzip.GzipFile(mode='r', fileobj=io)
        self.assertEqual(f.read(), '<h1>Hello dummy</h1>')

import colander
from wiseguy import WSGIComponent

from cStringIO import StringIO
test_config_file = StringIO('''
    main:
      component: pipeline
      config:
        apps: [ compress, filter, dummy ]

    compress:
      component: gzip
      config:
        compress_level: 6

    filter:
       component: dummyfilter

    dummy:
      component: dummycomponent
      config: { foo: 4 }

    ''')

class DummySchema(colander.MappingSchema):
    foo = colander.SchemaNode(colander.Int())

class DummyFactory(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, environ, start_response):
        from webob import Response
        r = Response()
        r.body = '<h1>Hello dummy</h1>'
        return r(environ, start_response)

class DummyFilterFactory(object):

    def __init__(self, app, **kwargs):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

class DummyApp(object):
    pass

DummyComponent = WSGIComponent(
    schema = DummySchema(),
    factory = DummyFactory,
    )

DummyFilter = WSGIComponent(
    schema = colander.MappingSchema(),
    factory = DummyFilterFactory,
    )

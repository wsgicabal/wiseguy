from wiseguy.loader import AppLoader
import unittest

class TestAppLoaderFunctional(unittest.TestCase):
    def test_it(self):
        c = AppLoader()
        c.add_component('dummyfilter', DummyFilter)
        c.add_component('dummycomponent', DummyComponent)
        c.load_yaml(test_config_file)
        app = c.load_app('main')
        self.failUnless(app)

import colander

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
        print 'DummyFactory called with %r' % kwargs

    def __call__(self, environ, start_response):
        from webob import Response
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

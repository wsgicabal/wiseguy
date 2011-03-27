import unittest

from wiseguy import WSGIComponent

class TestAppLoaderFunctional(unittest.TestCase):
    def test_it(self):
        from StringIO import StringIO
        import webob
        import gzip
        import paste.gzipper
        from wiseguy.loader import AppLoader
        from wiseguy.components.helloworld import HelloWorldFactory
        loader = AppLoader()
        loader.add_component('dummyfilter', DummyFilter)
        loader.load_yaml(test_config_file)
        app_factory = loader.get_app_factory('main')
        app = app_factory()
        self.assertEqual(app.__class__, paste.gzipper.middleware)
        self.assertEqual(app.application.__class__, DummyFilterFactory)
        self.assertEqual(app.application.app.__class__, HelloWorldFactory)
        request = webob.Request.blank('/')
        request.environ['HTTP_ACCEPT_ENCODING'] = 'gzip'
        status, headerlist, body = request.call_application(app)
        self.assertEqual(status, '200 OK')
        self.assertEqual(headerlist,
                         [('Content-Type', 'text/html; charset=UTF-8'),
                          ('content-encoding', 'gzip'),
                          ('Content-Length', '58')])
        io = StringIO(body[0])
        f = gzip.GzipFile(mode='r', fileobj=io)
        self.assertEqual(f.read(),
                         '<html><body><h1>Hello world!</h1></body></html>')

from cStringIO import StringIO
test_config_file = StringIO('''
    main:
      component: pipeline
      config:
        apps: [ compress, filter, hello ]

    compress:
      component: gzip
      config:
        compress_level: 6

    filter:
       component: dummyfilter

    hello:
      component: helloworld
    ''')

class DummyFilterFactory(object):
    def __init__(self, app, **kwargs):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

DummyFilter = WSGIComponent(
    schema = None,
    factory = DummyFilterFactory,
    )

import test_schema
from wiseguy.loader import AppLoader

def test():
    from cStringIO import StringIO
    from wsgiref.simple_server import make_server
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
    c = AppLoader()
    c.add_component('dummyfilter', test_schema.DummyFilter)
    c.add_component('dummycomponent', test_schema.DummyComponent)
    c.load_yaml(test_config_file)
    main = c.load_app('main')

    httpd = make_server('', 8000, main())
    httpd.serve_forever()

if __name__ == '__main__':
    test()

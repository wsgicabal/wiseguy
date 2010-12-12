from cStringIO import StringIO

from wiseguy import ep

from yaml import load, Loader

ep_parser = ep.EPParser()

class AppLoader(object):

    def __init__(self):
        self.apps = {}
    
    def load_yaml(self, stream):
        configfile = load(stream, Loader=Loader)
        for app_name, defn in configfile.iteritems():
            component_name = defn['component']
            component_config = defn.get('config', {})
            component = ep_parser.get(component_name).load()
            schema = component.schema.bind(loader=self)
            self.apps[app_name] = dict(
                factory = component.factory,
                schema = schema,
                config = component_config)

    def load_app(self, app_name):
        app = self.apps[app_name]
        config = app['schema'].deserialize(app['config'])
        print 'Deserialize config for', app_name
        factory = app['factory']
        def result(*extra_args, **extra_kwargs):
            kwargs = dict(config)
            kwargs.update(extra_kwargs)
            return factory(*extra_args, **kwargs)
        return result

def test():
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
    c.load_yaml(test_config_file)
    main = c.load_app('main')

    httpd = make_server('', 8000, main())
    httpd.serve_forever()

if __name__ == '__main__':
    test()

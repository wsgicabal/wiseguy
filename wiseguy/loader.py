from yaml import load, Loader

from pkg_resources import iter_entry_points

class EPParser(object):
    EP_GROUP = 'wiseguy.component'

    def show(self):
        for point in list(iter_entry_points(self.EP_GROUP)):
            component_name = point.name
            schema = point.load()
            yield schema, component_name

    def get(self, name):
        for point in iter_entry_points(self.EP_GROUP, name):
            return point

class AppLoader(object):

    def __init__(self, ep_parser=None):
        if ep_parser is None:
            self.ep_parser = EPParser()
        else:
            self.ep_parser = ep_parser
        self.apps = {}
        # extra non-entry point components
        self.components = {}
    
    def load_yaml(self, stream):
        self.load(load(stream, Loader=Loader))
   
    def add_component(self, name, klass):
        self.components[name] = klass

    def load(self, config):
        for app_name, defn in config.iteritems():
            component_name = defn['component']
            component_config = defn.get('config', {})
            component = self.ep_parser.get(component_name)
            if component:
                component = component.load() 
            else:
                component = self.components[component_name]
            schema = component.schema.bind(loader=self)
            self.apps[app_name] = dict(
                factory = component.factory,
                schema = schema,
                config = component_config)

    def load_app(self, app_name):
        app = self.apps[app_name]
        config = app['schema'].deserialize(app['config'])
        factory = app['factory']
        def result(*extra_args, **extra_kwargs):
            kwargs = dict(config)
            kwargs.update(extra_kwargs)
            return factory(*extra_args, **kwargs)
        return result

from yaml import load

from pkg_resources import iter_entry_points

from wiseguy.schema import NoSchema

class EPParser(object):
    EP_GROUP = 'wiseguy.component'
    iter_entry_points = iter_entry_points # for testing

    def get_components(self):
        for point in list(self.iter_entry_points(self.EP_GROUP)):
            component_name = point.name
            component = point.load()
            yield component_name, component

class AppLoader(object):

    def __init__(self, ep_parser=None):
        if ep_parser is None:
            ep_parser = EPParser()
        self.ep_parser = ep_parser
        self.components = dict(self.ep_parser.get_components())
        self.app_factories = {}

    def add_component(self, name, klass):
        self.components[name] = klass

    def load_yaml(self, stream):
        if not hasattr(stream, 'read'):
            stream = open(stream, 'r')
        self.load(load(stream))

    def load(self, sections):
        for app_name, section in sections.items():
            component_name = section['component']
            config = section.get('config', {})
            component = self.components.get(component_name)
            if component is None:
                raise ValueError('No such component %r' % component_name)
            app_factory = AppFactory(
                name = app_name,
                component = component,
                config = config,
                loader = self,
                )
            self.app_factories[app_name] = app_factory

    def get_app_factory(self, app_name):
        return self.app_factories[app_name]

class AppFactory(object):
    def __init__(self, name, component, config, loader):
        self.name = name
        self.component = component
        self.config = config
        self.loader = loader

    def __call__(self, *arg, **kw):
        component = self.component
        config = self.config
        schema = component.schema
        if schema is None:
            schema = NoSchema()
        schema = schema.bind(loader=self.loader)
        deserialized_config = schema.deserialize(config)
        extended = dict(deserialized_config)
        extended.update(kw)
        return component.factory(*arg, **extended)

    

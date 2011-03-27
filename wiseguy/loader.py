import colander

from yaml import load

from pkg_resources import iter_entry_points
from pkg_resources import load_entry_point

from wiseguy.schema import NoSchema
from wiseguy import WSGIComponent

class EPParser(object):
    EP_GROUP = 'wiseguy.component'
    PASTE_EP_GROUPS = ('paste.filter_app_factory', 'paste.app_factory')
    # we do not support paste.composite_factory entry points
    iter_entry_points = iter_entry_points # for testing

    def get_components(self):
        for point in list(self.iter_entry_points(self.EP_GROUP)):
            component_name = point.name
            component = point.load()
            yield component_name, component

    def load_entrypoint(self, ep_name, type_name=None):
        point = 'main'
        if '#' in ep_name:
            ep_name, point = ep_name.split('#', 1)
        if type_name is not None:
            groups = (type_name,)
        else:
            groups = (self.EP_GROUP,) + self.PASTE_EP_GROUPS
        for group in groups:
            try:
                return group, load_entry_point(ep_name, group, point)
            except ImportError:
                continue
        raise ValueError('No such entrypoint %r' % ep_name)

class AppLoader(object):
    def __init__(self, ep_parser=None):
        if ep_parser is None:
            ep_parser = EPParser()
        self.ep_parser = ep_parser
        self.components = dict(self.ep_parser.get_components())
        self.app_factories = {}
        self.global_object_getter = colander.GlobalObject(None)

    def add_component(self, name, klass):
        self.components[name] = klass

    def load_yaml(self, stream):
        if not hasattr(stream, 'read'):
            stream = open(stream, 'r')
        self.load(load(stream))

    def load(self, sections):
        for app_name, section in sections.items():
            component_name = section['component']
            type_name = section.get('type') # optional type hint
            config = section.get('config', {})
            # assume it's a config-file defined section name
            component = self.components.get(component_name)
            if component is None:
                if component_name.startswith('egg:'):
                    # also could be an 'egg:' URI
                    dist_name = component_name[len('egg:'):]
                    type_name, component = self.ep_parser.load_entrypoint(
                        dist_name, type_name)
                else:
                    # also could be a dotted.object.name or a dotted.object:name
                    component = self.global_object_getter.deserialize(
                        None, component_name)
                if type_name == 'paste.filter_app_factory':
                    # we can handle wiseguy components and paste middleware
                    # factories directly
                    component = WSGIComponent(
                        schema=None,
                        factory = pastefilter(component),
                        )
                elif type_name == 'paste.app_factory':
                    # ... but paste app factories want this stupid global
                    # conf value
                    component = WSGIComponent(
                        schema=None,
                        factory = pasteapp(component),
                        )
            if not is_wsgi_component(component):
                # it's not a WSGIComponent, it's just a plain app factory or
                # middleware factory; we wrap it in a WSGIComponent to
                # appease the framework
                component = WSGIComponent(
                    schema = None,
                    factory = component,
                    )
            app_factory = AppFactory(
                name = app_name,
                component = component,
                config = config,
                loader = self,
                )
            self.app_factories[app_name] = app_factory

    def get_app_factory(self, app_name):
        # could be a plain config-file-defined name
        return self.app_factories[app_name]

def pasteapp(factory):
    def inner(*arg, **kw):
        return factory({}, *arg, **kw)
    return inner

def pastefilter(factory):
    def inner(*arg, **kw):
        return factory(arg[0], {}, *arg[1:], **kw)
    return inner

def is_wsgi_component(ob):
    if  hasattr(ob, 'schema') and hasattr(ob, 'factory'):
        return True
    return False

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

    

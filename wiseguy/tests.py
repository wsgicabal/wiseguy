import colander

class DummySchema(colander.MappingSchema):
    foo = colander.SchemaNode(colander.Int())

class DummyFactory(object):

    def __init__(self, **kwargs):
        print 'DummyFactory called with %r' % kwargs

    def __call__(self, environ, start_response):
        pass

class DummyApp(object):
    pass

class DummyComponent(object):
    schema = DummySchema()
    factory = DummyFactory

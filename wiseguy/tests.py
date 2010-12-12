import colander

class DummySchema(colander.MappingSchema):
    foo = colendar.SchemaNode(colander.Int())

class DummyFactory(object):
    pass

class DummyApp(object):
    pass

class DummyComponent(object):
    schema = DummySchema()
    factory = DummyFactory()

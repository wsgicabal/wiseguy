import sys
import colander

@colander.deferred
def app_type(node, kw):
    return WSGIApp(loader=kw['loader'])

class WSGIApp(colander.SchemaType):

    def __init__(self, loader):
        self.loader = loader

    def deserialize(self, node, cstruct):
        if not cstruct:
            raise colander.Invalid(node, colander._('Required'))

        try:
            r = self.loader.load_app(cstruct)
            return r
        except Exception:
            raise
            e = sys.exc_info()[1]
            raise colander.Invalid(
                node,
                colander._('"${val}" is invalid (${err})',
                           mapping={'val':cstruct, 'err': e})
                )

class Apps(colander.SequenceSchema):
    app = colander.SchemaNode(app_type)

class WiseSchema(colander.Schema):

    @classmethod
    def schema_type(cls):
        return colander.Mapping(unknown='raise')
    
class PipelineSchema(WiseSchema):
    apps = Apps()

def PipelineFactory(apps, **config):
    app = apps[-1]()
    for filter in apps[-2::-1]:
        app = filter(app)
    return app

class WSGIComponent(object):
    def __init__(self, schema, factory):
        self.schema = schema
        self.factory = factory

PipelineComponent = WSGIComponent(
    schema=PipelineSchema(),
    factory=PipelineFactory)


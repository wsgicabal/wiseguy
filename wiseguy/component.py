import sys
import colander
import paste.gzipper
from translationstring import TranslationStringFactory

_ = TranslationStringFactory('wiseguy')

class StrictSchema(colander.Schema):
    @classmethod
    def schema_type(cls):
        return colander.Mapping(unknown='raise')
    
class WSGIComponent(object):
    def __init__(self, schema, factory):
        self.schema = schema
        self.factory = factory

@colander.deferred
def WSGIApp(node, kw):
    return _WSGIApp(loader=kw['loader'])

class _WSGIApp(colander.SchemaType):
    def __init__(self, loader):
        self.loader = loader

    def deserialize(self, node, cstruct):
        # cstruct is app name
        if not cstruct:
            raise colander.Invalid(node, _('Required'))

        try:
            app_factory = self.loader.get_app_factory(cstruct)
            return app_factory
        except Exception:
            e = sys.exc_info()[1]
            raise colander.Invalid(
                node,
                _('"${val}" is invalid (${err})',
                  mapping={'val':cstruct, 'err': e})
                )

class Apps(colander.SequenceSchema):
    app = colander.SchemaNode(WSGIApp)

class PipelineSchema(StrictSchema):
    apps = Apps()

def pipeline_factory(apps):
    app = apps[-1]()
    for middleware in apps[-2::-1]:
        app = middleware(app)
    return app

class GZipSchema(StrictSchema):
    compress_level = colander.SchemaNode(
        colander.Int(),
        missing=6,
        )

PipelineComponent = WSGIComponent(
    schema=PipelineSchema(),
    factory=pipeline_factory,
    )

GZipComponent = WSGIComponent(
    schema=GZipSchema(),
    factory=paste.gzipper.middleware,
    )

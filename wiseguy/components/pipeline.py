import colander

from wiseguy import StrictSchema
from wiseguy import _
from wiseguy import WSGIComponent

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
        except Exception, e:
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

PipelineComponent = WSGIComponent(
    schema=PipelineSchema(),
    factory=pipeline_factory,
    )

import sys
import colander
from . import schemas

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
    
class PipelineSchema(colander.MappingSchema):
    apps = Apps()

class PipelineFactory(object):

    def __init__(self, apps, **config):
        print 'PipelineFactory called with %r' % config
        app = apps[-1]()
        self.pipeline = [ app ]
        for filter in apps[-2::-1]:
            app = filter(app)
            self.pipeline.append(app)
        self.pipeline.reverse()
        self.app = app

    def __repr__(self):
        return 'Pipeline: %s' % '|'.join(map(repr, self.pipeline))

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
    
class PipelineComponent(object):
    schema = PipelineSchema()
    factory = PipelineFactory

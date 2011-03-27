"""
main:
    component: pipeline
    config:
        apps: [ compress, filter, dummy ]

"""
import colander

from wiseguy import StrictSchema
from wiseguy import WSGIComponent
from wiseguy import WSGIApp

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

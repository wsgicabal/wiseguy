"""
main:
    component: cascade
    config:
        apps: [ compress, filter, dummy ]
        catch: [ 404 ]
"""
import colander
from paste.cascade import Cascade

from wiseguy import StrictSchema
from wiseguy import WSGIComponent
from wiseguy import WSGIApp

class Apps(colander.SequenceSchema):
    app = colander.SchemaNode(WSGIApp)

class Catch(colander.SequenceSchema):
    code = colander.SchemaNode(colander.Int())

class CascadeSchema(StrictSchema):
    apps = Apps()
    catch = Catch(missing=[404])

def cascade_factory(apps, catch):
    apps = [app() for app in apps]
    return Cascade(apps, catch=catch)

CascadeComponent = WSGIComponent(
    schema=CascadeSchema(),
    factory=cascade_factory,
    )

import colander
from wiseguy import component

import paste.gzipper
class GZipSchema(component.WiseSchema):
    compress_level = colander.SchemaNode(
        colander.Int(),
        missing=6)
GZipComponent = component.WSGIComponent(
    schema=GZipSchema(),
    factory=paste.gzipper.middleware)

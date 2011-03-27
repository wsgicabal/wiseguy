"""
compress:
    component: gzip
    config:
        compress_level: 6
"""
import colander
import paste.gzipper

from wiseguy import StrictSchema
from wiseguy import WSGIComponent

class GZipSchema(StrictSchema):
    compress_level = colander.SchemaNode(
        colander.Int(),
        validator=colander.Range(1, 9),
        missing=6,
        default=6,
        )

GZipComponent = WSGIComponent(
    schema=GZipSchema(),
    factory=paste.gzipper.middleware,
    )

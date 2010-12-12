import colander
from . import schemas

class WSGIComponent(object):
    """
    A WSGI app or middleware.
    Must inherit this and set a 'schema'
    """
    
    def __init__(self, config):
        self.config = self.schema.deserialize(config)


class PipelineComponent(WSGIComponent):
    
    class PipelineSchema(colander.MappingSchema):
        apps = schemas.Apps()
    
    schema = PipelineSchema()

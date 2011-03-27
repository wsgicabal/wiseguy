import urlparse
import colander

from wiseguy import _

class StrictSchema(colander.Schema):
    @classmethod
    def schema_type(cls):
        return colander.Mapping(unknown='raise')

class NoSchema(colander.MappingSchema):
    @classmethod
    def schema_type(cls):
        return colander.Mapping(unknown='preserve')

class Url(colander.SchemaType):
    """
    returns a urlparse.ParseResult
    """
    
    def serialize(self, node, appstruct):
        if appstruct in (colander.null, None):
            return colander.null
        if isinstance(appstruct, basestring):
            appstruct = urlparse.urlparse(appstruct)
        
        try:
            return appstruct.geturl()
        except Exception:
            raise colander.Invalid(node,
                                   _('"${val}" is not a urlparse.ParseResult',
                                     mapping={'val':appstruct}),
                          )
    
    def deserialize(self, node, cstruct):
        if not cstruct:
            return colander.null

        try:
            r = urlparse.urlparse(cstruct)
            # require absolute urls
            if not r.scheme or not r.netloc or not r.hostname:
                raise Exception()
            # poke at stuff to make sure the parts are valid:
            r.port, r.username, r.password
            return r
        except Exception, e:
            raise colander.Invalid(node,
                                   _('"${val}" is not a URL (${err})',
                                     mapping={'val':cstruct, 'err': e})
                                   )


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


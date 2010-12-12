from colander import SchemaType, Invalid, null, Schema, SchemaNode, _
from colander import SequenceSchema, String, TupleSchema
import sys
import urlparse


#class App(String):
#    pass

#class Test(TupleSchema):
#    name = SchemaNode(String())

class Apps(SequenceSchema):
    app_name = SchemaNode(String())
    
class Url(SchemaType):
    """
    returns a urlparse.ParseResult
    """
    
    def serialize(self, node, appstruct):
        if appstruct is null:
            return null
        
        try:
            return appstruct.geturl()
        except Exception:
            raise Invalid(node,
                          _('"${val}" is not a urlparse.ParseResult',
                            mapping={'val':appstruct}),
                          )
    
    def deserialize(self, node, cstruct):
        if not cstruct:
            raise Invalid(node, _('Required'))

        try:
            r = urlparse.urlparse(cstruct)
            # require absolute urls
            if not r.scheme or not r.netloc or not r.hostname:
                raise Exception()
            # poke at stuff to make sure the parts are valid:
            r.port
            r.username
            r.password
            return r
        except Exception:
            e = sys.exc_info()[1]
            raise Invalid(node,
                          _('"${val}" is not a URL (${err})',
                            mapping={'val':cstruct, 'err': e})
                          )

    

def test_Url():
    class UrlSchema(Schema):
        url = SchemaNode(Url())
    
    #uri = "mysql://localhost:3306/?user=foo&password=bar"
    print UrlSchema().deserialize({'url': 'http://foo.com/asdf?x=y&b=z'})['url']
    try:
        UrlSchema().deserialize({'url': 'http://foo.com:badport/asdf'})
    except:
        pass
    else:
        raise Exception("should've got an exception for the invalid URL")
    
    
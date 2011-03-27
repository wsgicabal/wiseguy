from translationstring import TranslationStringFactory
_ = TranslationStringFactory('wiseguy')

from wiseguy.schema import StrictSchema # API
from wiseguy.schema import Url # API
from wiseguy.schema import WSGIApp # API

class WSGIComponent(object):
    def __init__(self, schema, factory):
        self.schema = schema
        self.factory = factory


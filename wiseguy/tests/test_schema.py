import unittest

from wiseguy import schema

class TestUrlType(unittest.TestCase):
    def _makeOne(self):
        return schema.Url()

    def test_deserialize_empty(self):
        import colander
        url = self._makeOne()
        result = url.deserialize(None, None)
        self.assertEqual(result, colander.null)

    def test_deserialize_ok(self):
        import urlparse
        expected = urlparse.ParseResult(
            scheme='http',
            netloc='foo.com',
            path='/asdf',
            params='',
            query='x=y&b=z',
            fragment='')
        url = self._makeOne()
        result = url.deserialize(None, 'http://foo.com/asdf?x=y&b=z')
        self.assertEqual(result, expected)

    def test_deserialize_failure(self):
        from colander import Invalid
        url = self._makeOne()
        self.assertRaises(Invalid, url.deserialize,
                          None, 'http://foo.com:badport/asdf')

    def test_deserialize_failure_notabsolute(self):
        from colander import Invalid
        url = self._makeOne()
        self.assertRaises(Invalid, url.deserialize,
                          None, '/asdf')

    def test_serialize_null(self):
        import colander
        url = self._makeOne()
        result = url.serialize(None, colander.null)
        self.assertEqual(result, colander.null)

    def test_serialize_str(self):
        url = self._makeOne()
        result = url.serialize(None, 'http://foo.com/asdf?x=y&b=z')
        self.assertEqual(result, 'http://foo.com/asdf?x=y&b=z')
        
    def test_serialize_ParseResult(self):
        import urlparse
        url = self._makeOne()
        inp = urlparse.ParseResult(
            scheme='http',
            netloc='foo.com',
            path='/asdf',
            params='',
            query='x=y&b=z',
            fragment='')
        result = url.serialize(None, inp)
        self.assertEqual(result, 'http://foo.com/asdf?x=y&b=z')

    def test_serialize_bogus(self):
        url = self._makeOne()
        from colander import Invalid
        self.assertRaises(Invalid, url.serialize, None, 1)

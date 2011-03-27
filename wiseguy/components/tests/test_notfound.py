import unittest

from wiseguy.components import notfound

class TestNotFoundFactory(unittest.TestCase):
    def _makeOne(self):
        return notfound.NotFoundFactory()
    
    def test_it(self):
        import webob
        app = self._makeOne()
        request = webob.Request.blank('/')
        status, headerlist, body = request.call_application(app)
        self.assertEqual(
            body[0].strip(),
            '404 Not Found\n\nThe resource could not be found.')
        self.assertEqual(status, '404 Not Found')
        self.assertEqual(
            headerlist,
             [('Content-Length', '52'),
              ('Content-Type', 'text/plain; charset=UTF-8')]
            )
        

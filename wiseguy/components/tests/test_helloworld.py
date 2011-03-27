import unittest

from wiseguy.components import helloworld

class TestHelloWorldFactory(unittest.TestCase):
    def _makeOne(self):
        return helloworld.HelloWorldFactory()
    
    def test_it(self):
        import webob
        app = self._makeOne()
        request = webob.Request.blank('/')
        status, headerlist, body = request.call_application(app)
        self.assertEqual(
            body,
            ['<html><body><h1>Hello world!</h1></body></html>'])
        self.assertEqual(status, '200 OK')
        self.assertEqual(
            headerlist,
            [('Content-Type', 'text/html; charset=UTF-8'),
             ('Content-Length', '47')]
            )
        

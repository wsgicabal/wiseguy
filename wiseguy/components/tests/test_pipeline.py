import unittest

from wiseguy.components import pipeline

class Test_WSGIApp(unittest.TestCase):
    def _makeOne(self, loader):
        return pipeline._WSGIApp(loader)

    def test_deserialize_bad_cstruct(self):
        from colander import Invalid
        loader = DummyLoader()
        inst = self._makeOne(loader)
        self.assertRaises(Invalid, inst.deserialize, None, None)

    def test_deserialize_loader_raises(self):
        from colander import Invalid
        loader = DummyRaisingLoader()
        inst = self._makeOne(loader)
        self.assertRaises(Invalid, inst.deserialize, None, 'abc')

    def test_deserialize_ok(self):
        loader = DummyLoader()
        inst = self._makeOne(loader)
        result = inst.deserialize(None, 'abc')
        self.assertEqual(result, 'abc')


class TestWSGIApp(unittest.TestCase):
    def _makeOne(self):
        return pipeline.WSGIApp(None, {'loader':DummyLoader()})

    def test_it(self):
        from wiseguy.components.pipeline import _WSGIApp
        inst = self._makeOne()
        self.assertEqual(inst.__class__, _WSGIApp)

class Test_pipeline_factory(unittest.TestCase):
    def _callFUT(self, apps):
        return pipeline.pipeline_factory(apps)

    def test_it(self):
        app1 = DummyApp()
        app2 = DummyApp()
        apps = [app1, app2]
        result = self._callFUT(apps)
        self.assertEqual(app1.args, (app2,))
        self.assertEqual(app2.args, ())
        self.assertEqual(result, app1)

class DummyLoader(object):
    def get_app_factory(self, cstruct):
        return cstruct

class DummyRaisingLoader(object):
    def get_app_factory(self, cstruct):
        raise RuntimeError

class DummyApp(object):
    def __call__(self, *args):
        self.args = args
        return self
    

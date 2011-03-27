import unittest

from wiseguy.components import pipeline

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

class DummyApp(object):
    def __call__(self, *args):
        self.args = args
        return self
    

import unittest

from wiseguy.components import cascade

class Test_cascade_factory(unittest.TestCase):
    def _callFUT(self, apps, catch):
        return cascade.cascade_factory(apps, catch)

    def test_it(self):
        app1 = DummyApp()
        app2 = DummyApp()
        apps = [app1, app2]
        result = self._callFUT(apps, [404, 405])
        self.assertEqual(result.apps, apps)
        self.assertEqual(sorted(result.catch_codes.keys()), [404, 405])

class DummyApp(object):
    def __call__(self, *args):
        self.args = args
        return self
    

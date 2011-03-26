import unittest

from wiseguy import loader

class TestEPParser(unittest.TestCase):
    def _makeOne(self):
        return loader.EPParser()

    def test_get_components(self):
        parser = self._makeOne()
        point = DummyPoint('name', 'component')
        def iter_entry_points(point_name):
            self.assertEqual(point_name, parser.EP_GROUP)
            return [point]
        parser.iter_entry_points = iter_entry_points
        generator = parser.get_components()
        self.assertEqual(list(generator), [('name', 'component')])

class TestAppLoader(unittest.TestCase):
    def _makeOne(self, ep_parser=None):
        return loader.AppLoader(ep_parser)

    def test_ctor_no_ep_parser(self):
        inst = self._makeOne()
        self.assertEqual(inst.ep_parser.__class__, loader.EPParser)
        self.failUnless(inst.components) # default gzip and pipeline registered
        self.assertEqual(inst.app_factories, {})
        
    def test_ctor_with_ep_parser(self):
        ep_parser = DummyEPParser()
        inst = self._makeOne(ep_parser)
        self.assertEqual(inst.ep_parser, ep_parser)
        self.assertEqual(inst.components, {})
        self.assertEqual(inst.app_factories, {})

    def test_add_component(self):
        ep_parser = DummyEPParser()
        inst = self._makeOne(ep_parser)
        inst.add_component('component', 'abc')
        self.assertEqual(inst.components['component'], 'abc')

class DummyPoint(object):
    def __init__(self, name, component):
        self.name = name
        self.component = component
        
    def load(self):
        return self.component
    
class DummyEPParser(object):
    def get_components(self):
        return ()
    

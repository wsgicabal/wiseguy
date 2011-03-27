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
        inst = self._makeOne()
        inst.add_component('component', 'abc')
        self.assertEqual(inst.components['component'], 'abc')

    def test_load_yaml_fileobj(self):
        from StringIO import StringIO
        inst = self._makeOne()
        inst.components['dummycomponent'] = '123'
        L = []
        inst.load = lambda *arg: L.append(arg)
        io = StringIO("""\
 main:
  component: dummycomponent
  config: { foo: 4 }""")
        inst.load_yaml(io)
        self.assertEqual(
            L,
            [({'main':
               {'component': 'dummycomponent',
                'config': {'foo': 4}}},)]
            )

    def test_load_yaml_filename(self):
        import tempfile
        f = tempfile.NamedTemporaryFile()
        f.write("""\
 main:
  component: dummycomponent
  config: { foo: 4 }""")
        f.flush()
        inst = self._makeOne()
        inst.components['dummycomponent'] = '123'
        L = []
        inst.load = lambda *arg: L.append(arg)
        inst.load_yaml(f.name)
        self.assertEqual(
            L,
            [({'main':
               {'component': 'dummycomponent',
                'config': {'foo': 4}}},)]
            )
        f.close()

    def test_load(self):
        sections = {'main':
                    {'component': 'dummycomponent',
                     'config': {'foo': 4}}}
        inst = self._makeOne()
        inst.components['dummycomponent'] = '123'
        inst.load(sections)
        self.assertEqual(
            inst.app_factories['main'].name,
            'main'
            )

    def test_load_nosuchcomponent(self):
        sections = {'main':
                    {'component': 'dummycomponent',
                     'config': {'foo': 4}}}
        inst = self._makeOne()
        self.assertRaises(ValueError, inst.load, sections)

    def test_get_app_factory(self):
        inst = self._makeOne()
        inst.app_factories['main'] = '123'
        self.assertEqual(inst.get_app_factory('main'), '123')

class TestAppFactory(unittest.TestCase):
    def _makeOne(self, name, component, config, ldr):
        return loader.AppFactory(name, component, config, ldr)

    def test_call(self):
        name = 'main'
        component = DummyComponent()
        config = {'a':1}
        ldr = 'loader'
        inst = self._makeOne(name, component, config, ldr)
        result = inst('123', b=1)
        self.assertEqual(result, 'abc')
        self.assertEqual(component.schema.bound, {'loader':'loader'})
        self.assertEqual(component.factoryargs, (('123',), {'a': 1, 'b': 1}))

class DummySchema(object):
    def bind(self, **kw):
        self.bound = kw
        return self

    def deserialize(self, value):
        return value

class DummyComponent(object):
    def __init__(self):
        self.schema = DummySchema()

    def factory(self, *arg, **kw):
        self.factoryargs = arg, kw
        return 'abc'

class DummyPoint(object):
    def __init__(self, name, component):
        self.name = name
        self.component = component
        
    def load(self):
        return self.component
    
class DummyEPParser(object):
    def get_components(self):
        return ()
    

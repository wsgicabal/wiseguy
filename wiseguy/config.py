from yaml import load, dump
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .component import WSGIComponent, PipelineComponent

class Config(object):
    
    def __init__(self, components):
        self.components = components

    def load_yaml(self, stream, comp_name='main'): # always start with 'main'?
        config = load(stream, Loader=Loader)
        from pprint import pprint
        #pprint(config)
        self.load(config, comp_name)
    
    def load(self, config, comp_name):
        comp_type = config[comp_name]['component']
        comp_config = config[comp_name].get('config', {})
        comp = self.components[comp_type](comp_config)
        #"""
        print comp
        print comp.config
        print comp.config['apps']
        print comp.config['apps'][0]
        print type(comp.config['apps'][0])
        #"""
        

def test():
    c = Config(components = {
        'pipeline': PipelineComponent,
        #'auth-middleware': MyComponent(),
    })
    from os.path import dirname
    c.load_yaml(open(dirname(__file__)+'/../foo.yml'))
        
    assert False
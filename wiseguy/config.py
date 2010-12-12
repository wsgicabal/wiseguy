from wiseguy import ep

from yaml import load, dump
from yaml import Loader, Dumper

ep_parser = ep.EPParser()

class Config(object):
    
    def load_yaml(self, stream):
        config = load(stream, Loader=Loader)
        self.config = config

    def load_app(self, name):
        app_factory_factory = ep_parser.get(name).load()
        import pdb; pdb.set_trace()


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
    c = Config()
    from os.path import dirname
    c.load_yaml(open(dirname(__file__)+'/../foo.yml'))
    c.load_app('main')
        
    assert False


if __name__ == '__main__':
    test()

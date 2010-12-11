from pkg_resources import iter_entry_points

class EPParser(object):
    EP_GROUP = 'wiseguy.component'

    def show(self):
        for point in list(iter_entry_points(self.EP_GROUP)):
            component_name = point.name
            schema = point.load()
            yield schema, component_name
            

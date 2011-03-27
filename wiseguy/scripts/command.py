import optparse
from wiseguy.loader import EPParser
from wiseguy.loader import AppLoader

from wsgiref.simple_server import make_server

class HelpFormatter(optparse.IndentedHelpFormatter):

    def format_description(self, description):
        return '%s\n' % description

def serve(app):
    server = make_server('', 8080, app)
    sa = server.socket.getsockname()
    print "Serving %s on" % app, sa[0], "port", sa[1], "..."
    server.serve_forever()

def main(argv=None):
    if argv is None:
        import sys
        argv = sys.argv

    parser = optparse.OptionParser(description=__doc__,
                                   formatter=HelpFormatter(),
                                  )

    parser.add_option('--list', dest='list_components',
        action='store_true', default=False,
        help="List available components")

    options, args = parser.parse_args(argv[1:])

    if args:
        if args[0] == 'webconfig':
            from wiseguy.web.app import configurator
            serve(configurator)

        if args[0] == 'serve':
            filename = args[1]
            loader = AppLoader()
            loader.load_yaml(filename)
            app_factory = loader.get_app_factory('main')
            app = app_factory()
            serve(app)

    if options.list_components:
        ep_parser = EPParser()
        for component_name, component in ep_parser.get_components():
            print component_name, component

if __name__ == '__main__':
    import sys
    main(sys.argv)

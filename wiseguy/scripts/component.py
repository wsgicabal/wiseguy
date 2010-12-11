import optparse
from wiseguy.ep import EPParser

class HelpFormatter(optparse.IndentedHelpFormatter):

    def format_description(self, description):
        return '%s\n' % description

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

    if options.list_components:
        ep_parser = EPParser()
        for schema, component_name in ep_parser.show():
            print schema, component_name

if __name__ == '__main__':
    import sys
    main(sys.argv)

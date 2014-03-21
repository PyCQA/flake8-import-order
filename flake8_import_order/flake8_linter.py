import flake8_import_order
from flake8_import_order import ImportOrderChecker


class Linter(ImportOrderChecker):
    name = "import-order"
    version = flake8_import_order.__version__

    def __init__(self, tree, filename):
        super(Linter, self).__init__(filename, tree)

    @classmethod
    def add_options(cls, parser):
        # List of application import names. They go last.
        parser.add_option(
            "--application-import-names",
            default="",
            action="store",
            type="string",
            help="Import names to consider as application specific"
        )
        parser.config_options.append("application-import-names")

    @classmethod
    def parse_options(cls, options):
        optdict = {}

        names = options.application_import_names.split(",")
        optdict['application_import_names'] = [n.strip() for n in names]

        cls.options = optdict

    def error(self, node, code, message):
        lineno, col_offset = node.lineno, node.col_offset
        return (lineno, col_offset, '{0} {1}'.format(code, message), Linter)

    def run(self):
        for error in self.check_order():
            yield error

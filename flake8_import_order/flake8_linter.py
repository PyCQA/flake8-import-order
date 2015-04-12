from __future__ import absolute_import

import flake8_import_order
from flake8_import_order import DEFAULT_IMPORT_ORDER_STYLE, ImportOrderChecker


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
        parser.add_option(
            "--import-order-style",
            default=DEFAULT_IMPORT_ORDER_STYLE,
            action="store",
            type="string",
            help="Style to follow. Available: cryptography, google"
        )
        parser.config_options.append("application-import-names")
        parser.config_options.append("import-order-style")

    @classmethod
    def parse_options(cls, options):
        optdict = {}

        names = options.application_import_names.split(",")
        optdict = dict(
            application_import_names=[n.strip() for n in names],
            import_order_style=options.import_order_style,
        )

        cls.options = optdict

    def error(self, node, code, message):
        lineno, col_offset = node.lineno, node.col_offset
        return (lineno, col_offset, '{0} {1}'.format(code, message), Linter)

    def run(self):
        for error in self.check_order():
            yield error

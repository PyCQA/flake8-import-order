import ast

import pycodestyle

from flake8_import_order import ImportVisitor
from flake8_import_order.styles import (
    AppNexus, Cryptography, Google, PEP8, Smarkets,
)

DEFAULT_IMPORT_ORDER_STYLE = 'cryptography'


class ImportOrderChecker(object):
    visitor_class = ImportVisitor
    options = None

    def __init__(self, filename, tree):
        self.tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    def error(self, error):
        raise NotImplemented()

    def check_order(self):
        if not self.tree or not self.lines:
            self.load_file()

        style_option = self.options.get(
            'import_order_style', DEFAULT_IMPORT_ORDER_STYLE,
        )

        # application_package_names is supported only for the 'appnexus' style
        if style_option == 'appnexus':
            visitor = self.visitor_class(
                self.options.get('application_import_names', []),
                self.options.get('application_package_names', []),
            )
        else:
            visitor = self.visitor_class(
                self.options.get('application_import_names', []),
                [],
            )
        visitor.visit(self.tree)

        imports = []
        for import_ in visitor.imports:
            if not pycodestyle.noqa(self.lines[import_.lineno - 1]):
                imports.append(import_)

        if style_option == 'cryptography':
            style = Cryptography(imports)
        elif style_option == 'google':
            style = Google(imports)
        elif style_option == 'pep8':
            style = PEP8(imports)
        elif style_option == 'smarkets':
            style = Smarkets(imports)
        elif style_option == 'appnexus':
            style = AppNexus(imports)
        else:
            raise AssertionError("Unknown style {}".format(style_option))

        for error in style.check():
            yield self.error(error)

import ast

import pycodestyle

from flake8_import_order import ImportVisitor
from flake8_import_order.styles import lookup_entry_point

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
        return error

    def check_order(self):
        if not self.tree or not self.lines:
            self.load_file()

        try:
            style_entry_point = self.options['import_order_style']
        except KeyError:
            style_entry_point = lookup_entry_point(DEFAULT_IMPORT_ORDER_STYLE)

        # application_package_names is supported only for the
        # 'appnexus' and 'edited' styles
        if style_entry_point.name in ['appnexus', 'edited']:
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

        style_cls = style_entry_point.load()
        style = style_cls(imports)

        for error in style.check():
            yield self.error(error)

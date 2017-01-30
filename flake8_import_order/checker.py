import ast

import pkg_resources

import pycodestyle

from flake8_import_order import ImportVisitor

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

        style_option = self.options.get(
            'import_order_style', DEFAULT_IMPORT_ORDER_STYLE,
        )

        # application_package_names is supported only for the
        # 'appnexus' and 'edited' styles
        if style_option in ['appnexus', 'edited']:
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

        try:
            style_entry_point = next(
                pkg_resources.iter_entry_points(
                    'flake8_import_order.styles',
                    name=style_option
                )
            )
        except StopIteration:
            raise AssertionError("Unknown style {}".format(style_option))
        else:
            style_cls = style_entry_point.load()
            style = style_cls(imports)

        for error in style.check():
            yield self.error(error)

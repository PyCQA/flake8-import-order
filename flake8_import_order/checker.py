import ast

import asttokens

import pycodestyle

from flake8_import_order import ImportVisitor
from flake8_import_order.styles import lookup_entry_point

DEFAULT_IMPORT_ORDER_STYLE = 'cryptography'


class ImportOrderChecker(object):
    visitor_class = ImportVisitor
    options = None

    def __init__(self, filename, tree):
        self.ast_tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if self.ast_tree is None:
            self.ast_tree = ast.parse(''.join(self.lines))

    def error(self, error):
        return error

    def check_order(self):
        if not self.ast_tree or not self.lines:
            self.load_file()

        tree = asttokens.ASTTokens(
            ''.join(self.lines), parse=False, tree=self.ast_tree,
        ).tree

        try:
            style_entry_point = self.options['import_order_style']
        except KeyError:
            style_entry_point = lookup_entry_point(DEFAULT_IMPORT_ORDER_STYLE)
        style_cls = style_entry_point.load()

        if style_cls.accepts_application_package_names:
            visitor = self.visitor_class(
                self.options.get('application_import_names', []),
                self.options.get('application_package_names', []),
            )
        else:
            visitor = self.visitor_class(
                self.options.get('application_import_names', []),
                [],
            )
        visitor.visit(tree)

        style = style_cls(visitor.imports)

        for error in style.check():
            if not pycodestyle.noqa(self.lines[error.lineno - 1]):
                yield self.error(error)

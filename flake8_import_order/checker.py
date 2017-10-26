import asttokens
import pycodestyle

from flake8_import_order import ImportVisitor
from flake8_import_order.styles import lookup_entry_point

DEFAULT_IMPORT_ORDER_STYLE = 'cryptography'


class ImportOrderChecker(object):
    visitor_class = ImportVisitor
    options = None

    def __init__(self, filename):
        self.filename = filename
        self.lines = None
        self.tree = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        self.tree = asttokens.ASTTokens(''.join(self.lines), parse=True).tree

    def error(self, error):
        return error

    def check_order(self):
        if not self.tree or not self.lines:
            self.load_file()

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
        visitor.visit(self.tree)

        imports = []
        for import_ in visitor.imports:
            if not pycodestyle.noqa(self.lines[import_.start_line - 1]):
                imports.append(import_)

        style = style_cls(imports)

        for error in style.check():
            yield self.error(error)

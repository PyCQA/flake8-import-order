import ast
import re

import asttokens

import pycodestyle

from flake8_import_order import ImportVisitor
from flake8_import_order.styles import lookup_entry_point

DEFAULT_IMPORT_ORDER_STYLE = 'cryptography'
NOQA_INLINE_REGEXP = re.compile(
    # We're looking for items that look like this:
    # ``# noqa``
    # ``# noqa: E123``
    # ``# noqa: E123,W451,F921``
    # ``# NoQA: E123,W451,F921``
    # ``# NOQA: E123,W451,F921``
    # We do not care about the ``: `` that follows ``noqa``
    # We do not care about the casing of ``noqa``
    # We want a comma-separated list of errors
    '# noqa(?:: (?P<codes>([A-Z][0-9]+(?:[,\s]+)?)+))?',
    re.IGNORECASE
)
COMMA_SEPARATED_LIST_RE = re.compile(r'[,\s]')


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
            if not self.error_is_ignored(error):
                yield self.error(error)

    def error_is_ignored(self, error):
        noqa_match = NOQA_INLINE_REGEXP.search(self.lines[error.lineno - 1])
        if noqa_match is None:
            return False

        codes_str = noqa_match.groupdict()['codes']
        if codes_str is None:
            return True

        codes = set(parse_comma_separated_list(codes_str))
        if error.code in codes:
            return True

        return False


def parse_comma_separated_list(value):
    value = COMMA_SEPARATED_LIST_RE.split(value)
    item_gen = (item.strip() for item in value)
    return [item for item in item_gen if item]

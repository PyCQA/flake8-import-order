import ast

from pylama.lint import Linter as BaseLinter

from flake8_import_order import (
    ImportOrderChecker,
    ImportVisitor
)


class Linter(ImportOrderChecker):
    name = "import-order"
    version = "0.1"

    def __init__(self):
        super(Linter, self).__init__()

    def allow(self, path):
        return path.endswith(".py")

    def error(self, node, code, message):
        lineno, col_offset = node.lineno, node.col_offset
        return {
            "lnum": lineno,
            "col": col_offset,
            "text": message,
            "type": code
        }

    def run(self, path, **meta):
        data = open(path).read()
        self.tree = ast.parse(data, path)

        for error in self.check_order():
            yield error

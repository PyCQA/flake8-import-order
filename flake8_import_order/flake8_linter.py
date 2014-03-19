from flake8_import_order import ImportOrderChecker


class Linter(ImportOrderChecker):
    name = "import-order"
    version = "0.1"

    def __init__(self, tree, filename):
        super(Linter, self).__init__(filename, tree)

    def error(self, node, code, message):
        lineno, col_offset = node.lineno, node.col_offset
        return (lineno, col_offset, '{0} {1}'.format(code, message), Linter)

    def run(self):
        for error in self.check_order():
            yield error

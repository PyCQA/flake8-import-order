import ast
from collections import namedtuple

from flake8_import_order.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__,
)
from flake8_import_order.stdlib_list import STDLIB_NAMES

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
]

DEFAULT_IMPORT_ORDER_STYLE = 'cryptography'

IMPORT_FUTURE = 0
IMPORT_STDLIB = 10
IMPORT_3RD_PARTY = 20
IMPORT_APP_PACKAGE = 30
IMPORT_APP = 40
IMPORT_APP_RELATIVE = 50
IMPORT_MIXED = -1

ClassifiedImport = namedtuple(
    'ClassifiedImport',
    ['type', 'is_from', 'modules', 'names', 'lineno', 'level', 'package'],
)


def root_package_name(name):
    p = ast.parse(name)
    for n in ast.walk(p):
        if isinstance(n, ast.Name):
            return n.id
    else:
        return None


class ImportVisitor(ast.NodeVisitor):

    def __init__(self, application_import_names, application_package_names):
        self.imports = []
        self.application_import_names = application_import_names
        self.application_package_names = application_package_names

    def visit_Import(self, node):  # noqa
        if node.col_offset == 0:
            modules = [alias.name for alias in node.names]
            types_ = {self._classify_type(module) for module in modules}
            if len(types_) == 1:
                type_ = types_.pop()
            else:
                type_ = IMPORT_MIXED
            classified_import = ClassifiedImport(
                type_, False, modules, [], node.lineno, 0,
                root_package_name(modules[0]),
            )
            self.imports.append(classified_import)

    def visit_ImportFrom(self, node):  # noqa
        if node.col_offset == 0:
            module = node.module or ''
            if node.level > 0:
                type_ = IMPORT_APP_RELATIVE
            else:
                type_ = self._classify_type(module)
            names = [alias.name for alias in node.names]
            classified_import = ClassifiedImport(
                type_, True, [module], names,
                node.lineno, node.level,
                root_package_name(module),
            )
            self.imports.append(classified_import)

    def _classify_type(self, module):
        package = root_package_name(module)

        if package == "__future__":
            return IMPORT_FUTURE
        elif package in self.application_import_names:
            return IMPORT_APP
        elif package in self.application_package_names:
            return IMPORT_APP_PACKAGE
        elif package in STDLIB_NAMES:
            return IMPORT_STDLIB
        else:
            # Not future, stdlib or an application import.
            # Must be 3rd party.
            return IMPORT_3RD_PARTY

import ast

from flake8_import_order.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
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
IMPORT_APP = 30
IMPORT_MIXED = -1


def root_package_name(name):
    p = ast.parse(name)
    for n in ast.walk(p):
        if isinstance(n, ast.Name):
            return n.id
    else:
        return None


def is_sorted(seq):
    return sorted(seq) == list(seq)


def lower_strings(l):
    return [e.lower() if hasattr(e, 'lower') else e for e in l]


class ImportVisitor(ast.NodeVisitor):
    """
    This class visits all the import nodes at the root of tree and generates
    sort keys for each import node.

    In practice this means that they are sorted according to something like
    this tuple.

        (stdlib, site_packages, names)
    """

    def __init__(self, filename, options):
        self.filename = filename
        self.options = options or {}
        self.imports = []

        self.application_import_names = set(
            self.options.get("application_import_names", [])
        )
        self.style = self.options['import_order_style']

    def visit_Import(self, node):  # noqa
        if node.col_offset != 0:
            return
        else:
            self.imports.append(node)
            return

    def visit_ImportFrom(self, node):  # noqa
        if node.col_offset != 0:
            return
        else:
            self.imports.append(node)
            return

    def node_sort_key(self, node):
        """
        Return a key that will sort the nodes in the correct
        order for the Google Code Style guidelines.
        """
        normalize_names = lower_strings if self.style == 'google' else list

        if isinstance(node, ast.Import):
            names = [nm.name for nm in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or '']
        else:
            raise TypeError(type(node))

        import_type = self._import_type(node, names[0])
        for name in names[1:]:
            name_type = self._import_type(node, name)
            if import_type != name_type:
                import_type = IMPORT_MIXED
                break

        names = normalize_names(names)

        imported_names = [
            normalize_names([nm.name, nm.asname]) for nm in node.names]
        is_star_import = not any(nm == "*" for nm, asnm in imported_names)
        from_level = getattr(node, "level", -1)

        n = (
            import_type,
            names,
            from_level,
            is_star_import,
            imported_names,
        )

        if n[0] == IMPORT_FUTURE:
            group = (n[0], None, None, None, n[4])
        elif n[0] == IMPORT_STDLIB or self.style == 'google':
            group = (n[0], n[2], n[1], n[3], n[4])
        elif n[0] == IMPORT_3RD_PARTY:
            group = (n[0], n[1], n[2], n[3], n[4])
        else:
            group = n

        return group

    def _import_type(self, node, name):
        if isinstance(name, int):
            return None

        if name is None:
            # relative import
            return IMPORT_APP

        pkg = root_package_name(name)

        # Entirely not confusingly we use "False" for "True" in the flags.

        if pkg == "__future__":
            return IMPORT_FUTURE

        elif (
            pkg in self.application_import_names or
            (isinstance(node, ast.ImportFrom) and node.level > 0)
        ):
            return IMPORT_APP

        elif pkg in STDLIB_NAMES:
            return IMPORT_STDLIB

        else:
            # Not future, stdlib or an application import.
            # Must be 3rd party.
            return IMPORT_3RD_PARTY


class ImportOrderChecker(object):
    visitor_class = ImportVisitor
    options = None

    def __init__(self, filename, tree):
        self.filename = filename
        self.tree = tree
        self.visitor = None

    def error(self, node, code, message):
        raise NotImplemented()

    def check_order(self):
        if not self.tree:
            self.tree = ast.parse(open(self.filename).read())

        self.visitor = self.visitor_class(self.filename, self.options)
        self.visitor.visit(self.tree)

        style = self.options['import_order_style']

        prev_node = None
        for node in self.visitor.imports:
            n = self.visitor.node_sort_key(node)

            if n[-1] and not is_sorted(n[-1]):
                yield self.error(
                    node, "I101",
                    "Imported names are in the wrong order"
                )

            if prev_node is None:
                prev_node = node
                continue

            pn = self.visitor.node_sort_key(prev_node)

            # FUTURES
            # STDLIBS, STDLIB_FROMS
            # 3RDPARTY[n], 3RDPARTY_FROM[n]
            # 3RDPARTY[n+1], 3RDPARTY_FROM[n+1]
            # APPLICATION, APPLICATION_FROM

            # import_type, names, is_from, level, imported_names,

            if n[0] == IMPORT_MIXED:
                yield self.error(
                    node, "I666",
                    "Import statement crosses types"
                )
                prev_node = node
                continue

            if n < pn:
                yield self.error(
                    node, "I100",
                    "Imports are in the wrong order"
                )

            lines_apart = node.lineno - prev_node.lineno

            if (
                (
                    n[0] != pn[0] or
                    (
                        n[0] == IMPORT_3RD_PARTY and
                        style != 'google' and
                        root_package_name(n[1][0]) !=
                        root_package_name(pn[1][0])
                    )
                ) and
                lines_apart == 1
            ):
                yield self.error(
                    node, "I201",
                    "Missing newline between sections or imports"
                )

            prev_node = node

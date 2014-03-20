try:
    import ast
except ImportError:
    from flake8.util import ast

from flake8_import_order.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)
from flake8_import_order.stdlib_list import STDLIB_NAMES


__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
]


class ImportVisitor(ast.NodeVisitor):
    """
    This class visits all the import nodes at the root of tree and generates
    sort keys for each import node.

    In practice this means that they are sorted according to something like
    this tuple.

        (stdlib, site_packages, names)
    """

    def __init__(self, filename):
        self.filename = filename
        self.original_nodes = []
        self.imports = []

        self.third_party_paths = [
            p for p in sys.path
            if p.endswith(".egg") or "-packages" in p
        ]

        self.local_paths = [""]
        file_dir = os.path.dirname(self.filename).split(os.sep)
        search_places = [file_dir[:n] for n in range(len(file_dir) + 1)]
        self.local_paths.extend(
            os.path.join(*path)
            for path in search_places if path
        )

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
        if isinstance(node, ast.Import):
            if node.names[0].asname:
                name = [node.names[0].name, node.names[0].asname]
            else:
                name = [node.names[0].name]
            from_names = None

        elif isinstance(node, ast.ImportFrom):
            name = [node.module]
            from_names = [nm.name for nm in node.names]
        else:
            raise TypeError(node)

        # stdlib, site package, name, from_names
        key = [True, True, name, from_names]

        if not name[0]:
            key[2] = [node.level]
        else:
            key[2] = name
            p = ast.parse(name[0])
            for n in ast.walk(p):
                if not isinstance(n, ast.Name):
                    continue

                if n.id in STDLIB_NAMES:
                    key[0] = False

                else:
                    try:
                        local_module = imp.find_module(
                            n.id,
                            self.local_paths
                        )
                    except ImportError:
                        local_module = None

                    try:
                        external_module = imp.find_module(
                            n.id,
                            self.third_party_paths
                        )
                    except ImportError:
                        external_module = None

                    if external_module and not local_module:
                        key[1] = False

        return key


class ImportOrderChecker(object):
    visitor_class = ImportVisitor

    def __init__(self, filename, tree):
        self.filename = filename
        self.tree = tree
        self.visitor = None

    def error(self, node, code, message):
        raise NotImplemented()

    def check_order(self):
        self.visitor = self.visitor_class(self.filename)
        self.visitor.visit(self.tree)

        prev_node = None
        for node in self.visitor.imports:
            if node and prev_node:
                node_key = self.visitor.node_sort_key(node)
                prev_node_key = self.visitor.node_sort_key(prev_node)

                if node_key[:2] < prev_node_key[:2]:
                    yield self.error(node, "I102",
                                     "Import is in the wrong section")

                elif node_key[-1] and sorted(node_key[-1]) != node_key[-1]:
                    yield self.error(node, "I101",
                                     "Imported names are in the wrong order")

                elif node_key < prev_node_key:
                    yield self.error(node, "I100",
                                     "Imports are in the wrong order")

            prev_node = node

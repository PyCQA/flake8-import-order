try:
    import ast
except ImportError:
    from flake8.util import ast

import imp
import sys

from flake8_import_order.stdlib_list import STDLIB_NAMES


class ImportVisitor(ast.NodeVisitor):
    """
    This class visits all the import nodes at the root of tree and generates
    sort keys for each import node.

    In practice this means that they are sorted according to something like
    this tuple.

        (stdlib, site_packages, names)
    """

    def __init__(self):
        self.original_nodes = []
        self.imports = []
        self.third_party_paths = [
            p for p in sys.path
            if p.endswith(".egg") or "-packages" in p
        ]

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

        # stdlib, site package, name, is_fromimport, from_names
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
                        key[1] = not imp.find_module(
                            n.id,
                            self.third_party_paths
                        )
                    except ImportError:
                        continue
        return key


class ImportOrderChecker(object):
    def __init__(self):
        self.visitor = ImportVisitor()
        self.tree = None

    def error(self, node, code, message):
        raise NotImplemented()

    def check_order(self):
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

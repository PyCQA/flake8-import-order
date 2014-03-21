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


def root_package_name(name):
    p = ast.parse(name)
    for n in ast.walk(p):
        if isinstance(n, ast.Name):
            return n.id
    else:
        return None


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
        flag_union = [True, True, True]

        if isinstance(node, ast.Import):
            names = [nm.name for nm in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module]
        else:
            raise TypeError(type(node))

        imported_names = [[nm.name, nm.asname] for nm in node.names]

        # The key is a bit silly because we use False for "True" because we
        # want a list of keys to sort() in the order the nodes should go in
        # in the source.

        # [[is_future, is_stdlib, is_third_party],
        # homogenous, [name], [imported]]
        key = [
            flag_union,
            True, names, getattr(node, "level", -1), imported_names
        ]

        # You can have multiple names in one import statement. We just find the
        # union of all flags that the names share.
        all_flags = set()
        for name in names:
            flags = self._name_flags(node, name)
            if flags is not None:
                all_flags.add(flags)

        # Detect if all names had the same flags
        # key[1] = len(all_flags) == 1

        # Update flag_union
        all_flags = zip(*all_flags)
        for i, flags in enumerate(all_flags):
            flag_set = set(flags)
            if flag_set == set([False]):
                flag_union[i] = False
            else:
                flag_union[i] = True
        return key

    def _name_flags(self, node, name):
        if isinstance(name, int):
            return None

        pkg = root_package_name(name)

        flags = [True, True, True]
        if pkg == "__future__":
            flags[0] = False

        elif pkg in STDLIB_NAMES:
            flags[1] = False

        elif (
            pkg in self.application_import_names or
            (isinstance(node, ast.ImportFrom) and node.level > 0)
        ):
            flags[2] = True

        else:
            # Not future, stdlib or an application import.
            # Must be 3rd party.
            flags[2] = False

        return tuple(flags)


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
        self.tree = ast.parse(open(self.filename).read())

        self.visitor = self.visitor_class(self.filename, self.options)
        self.visitor.visit(self.tree)

        prev_node = None
        for node in self.visitor.imports:
            if node and prev_node:
                node_key = self.visitor.node_sort_key(node)
                prev_node_key = self.visitor.node_sort_key(prev_node)

                if node_key[0] < prev_node_key[0]:
                    yield self.error(
                        node, "I102",
                        "Import is in the wrong section"
                    )

                elif node_key[-1] and sorted(node_key[-1]) != node_key[-1]:
                    yield self.error(
                        node, "I101",
                        "Imported names are in the wrong order"
                    )
                elif node_key < prev_node_key:
                    yield self.error(
                        node, "I100",
                        "Imports are in the wrong order"
                    )

                if (
                    # prev is __future__ or both stdlib
                    (
                        prev_node_key[0][0] is False or
                        (node_key[0][1] is True and
                         prev_node_key[0][1] is True)
                    ) and
                    # modules dont match
                    root_package_name(node_key[2][0]) !=
                        root_package_name(prev_node_key[2][0]) and
                    # are on consecutive lines
                    node.lineno - prev_node.lineno == 1
                ):
                    yield self.error(
                        node, "I103",
                        "Missing newline between sections or imports"
                    )

            prev_node = node

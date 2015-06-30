import ast

import pep8

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
IMPORT_APP_RELATIVE = 40
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
    if l is None:
        return None
    else:
        return [e.lower() if hasattr(e, 'lower') else e for e in l]


def cmp_values(n, style):
    if n[0] in (IMPORT_STDLIB, IMPORT_APP_RELATIVE) or style == "google":
        return [
            n[0],
            n[1],
            lower_strings(n[2]),
            n[3],
            [lower_strings(x) for x in n[4]]
        ]
    else:
        return [
            n[0],
            lower_strings(n[1]),
            n[2],
            n[3],
            [lower_strings(x) for x in n[4]]
        ]


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

        imported_names = [
            [nm.name if nm.name != "*"
             else "{0}.*".format(node.module), nm.asname]
            for nm in node.names
        ]

        if self.style == "google":
            true_from_level = getattr(node, "level", -1)

            if true_from_level == -1:
                from_level = 0
                is_not_star_import = False
            else:
                from_level = true_from_level
                is_not_star_import = (
                    not any(nm.endswith("*")
                            for nm, asnm in imported_names)
                )

        else:
            from_level = getattr(node, "level", -1)
            is_not_star_import = (
                not any(nm.endswith("*")
                        for nm, asnm in imported_names)
            )

        n = (
            import_type,
            names,
            from_level,
            is_not_star_import,
            imported_names,
        )

        if n[0] == IMPORT_FUTURE:
            group = (n[0], None, None, None, n[4])
        elif (
            n[0] in (IMPORT_STDLIB, IMPORT_APP_RELATIVE) or
            self.style == 'google'
        ):
            group = (n[0], n[2], n[1], n[3], n[4])
        elif n[0] == IMPORT_3RD_PARTY:
            group = (n[0], n[1], n[2], n[3], n[4])
        else:
            group = n

        return group, n

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

        elif pkg in self.application_import_names:
            return IMPORT_APP

        elif isinstance(node, ast.ImportFrom) and node.level > 0:
            return IMPORT_APP_RELATIVE

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
        self.tree = tree
        self.filename = filename
        self.lines = None

    def load_file(self):
        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pep8.stdin_get_value().splitlines(True)
        else:
            self.lines = pep8.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    def error(self, node, code, message):
        raise NotImplemented()

    def check_order(self):
        if not self.tree or not self.lines:
            self.load_file()

        visitor = self.visitor_class(self.filename, self.options)
        visitor.visit(self.tree)

        style = self.options['import_order_style']

        prev_node = None
        for node in visitor.imports:
            # Lines with the noqa flag are ignored entirely
            if pep8.noqa(self.lines[node.lineno - 1]):
                continue

            n, k = visitor.node_sort_key(node)

            if style == "google":
                cmp_n = cmp_values(n, style)
            else:
                cmp_n = n

            if cmp_n[-1] and not is_sorted(cmp_n[-1]):
                sort_key = lambda s: s[0]
                if style == "google":
                    sort_key = lambda s: s[0].lower()
                should_be = ", ".join(
                    name[0] for name in
                    sorted(n[-1], key=sort_key))
                yield self.error(
                    node, "I101",
                    (
                        "Imported names are in the wrong order. "
                        "Should be {0}".format(should_be)
                    )
                )

            if prev_node is None:
                prev_node = node
                continue

            pn, pk = visitor.node_sort_key(prev_node)

            if style == "google":
                cmp_pn = cmp_values(pn, style)
            else:
                cmp_pn = pn

            # FUTURES
            # STDLIBS, STDLIB_FROMS
            # 3RDPARTY[n], 3RDPARTY_FROM[n]
            # 3RDPARTY[n+1], 3RDPARTY_FROM[n+1]
            # APPLICATION, APPLICATION_FROM

            # import_type, names, level, is_star_import, imported_names,

            if n[0] == IMPORT_MIXED:
                yield self.error(
                    node, "I666",
                    "Import statement mixes groups"
                )
                prev_node = node
                continue

            if cmp_n < cmp_pn:
                def build_str(key):
                    level = key[2]
                    if level >= 0:
                        start = "from " + level * '.'
                    else:
                        start = "import "
                    return start + ", ".join(key[1])

                first_str = build_str(k)
                second_str = build_str(pk)

                yield self.error(
                    node, "I100",
                    (
                        "Imports statements are in the wrong order. "
                        "{0} should be before {1}".format(
                            first_str,
                            second_str
                        )
                    )
                )

            lines_apart = node.lineno - prev_node.lineno

            is_app = (
                set([cmp_n[0], cmp_pn[0]]) !=
                set([IMPORT_APP, IMPORT_APP_RELATIVE])
            )

            if lines_apart == 1 and ((
                cmp_n[0] != cmp_pn[0] and
                (style != "google" or is_app)
            ) or (
                n[0] == IMPORT_3RD_PARTY and
                style != 'google' and
                root_package_name(cmp_n[1][0]) !=
                root_package_name(cmp_pn[1][0])
            )):
                yield self.error(
                    node, "I201",
                    "Missing newline before sections or imports."
                )

            prev_node = node

import ast

import pycodestyle

from flake8_import_order.flake8_linter import Linter
from flake8_import_order.styles import Google


def test_parsing():
    style = 'google'
    import_names = ['flake8_import_order', 'tests']
    package_names = ['local_package']
    argv = [
        "--application-import-names={}".format(','.join(import_names)),
        "--import-order-style={}".format(style),
        "--application-package-names={}".format(','.join(package_names)),
    ]

    parser = pycodestyle.get_parser('', '')
    Linter.add_options(parser)
    options, args = parser.parse_args(argv)
    Linter.parse_options(options)

    assert Linter.options['import_order_style'].name == style
    assert Linter.options['import_order_style'].load() is Google
    assert Linter.options['application_import_names'] == import_names
    assert Linter.options['application_package_names'] == package_names


def test_linter():
    argv = ['--application-import-names=flake8_import_order']
    parser = pycodestyle.get_parser('', '')
    Linter.add_options(parser)
    options, args = parser.parse_args(argv)
    Linter.parse_options(options)

    data = 'import ast\nimport flake8_import_order\n'
    pycodestyle.stdin_get_value = lambda: data
    tree = ast.parse(data)
    checker = Linter(tree, None)
    for lineno, col_offset, msg, instance in checker.run():
        assert msg.startswith(
            'I201 Missing newline between import groups.',
        )

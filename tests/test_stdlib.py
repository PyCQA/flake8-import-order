import ast

import pycodestyle
import pytest

from flake8_import_order import STDLIB_NAMES
from flake8_import_order.flake8_linter import Linter


def _get_linter(argv, code, filename):
    parser = pycodestyle.get_parser('', '')
    Linter.add_options(parser)
    options, args = parser.parse_args(argv)
    Linter.parse_options(options)
    return Linter(
        ast.parse(
            code,
            filename
        ),
        str(filename)
    )


def pytest_generate_tests(metafunc):
    if 'stdlib_module' in metafunc.fixturenames:
        metafunc.parametrize(
            'stdlib_module',
            sorted(
                name
                for name in STDLIB_NAMES
                if not name.startswith("__")
            )
        )


@pytest.fixture(scope="module")
def tmpdir_single(tmpdir_factory):
    return tmpdir_factory.mktemp("stdlib_imports")


@pytest.mark.parametrize(
    'mode',
    (
        "cryptography",
        "google",
        "smarkets",
        "pep8"
    )
)
def test_stdlib_imports(tmpdir_single, mode, stdlib_module):
    argv = [
        "--import-order-style={0}".format(mode),
    ]

    test_file = tmpdir_single.join("test_{0}_{1}.py".format(stdlib_module, mode))
    test_file.write_text(u"import {0}\nimport zlib\n".format(stdlib_module), "UTF-8")

    checker = _get_linter(argv, test_file.read(), str(test_file))
    codes = []
    messages = []
    for lineno, col_offset, msg, instance in checker.run():
        code, message = msg.split(" ", 1)
        codes.append(code)
        messages.append("{0}: {1}".format(lineno, msg))
    assert messages == []
    assert codes == []

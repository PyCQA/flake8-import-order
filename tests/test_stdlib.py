import ast

import pycodestyle

import pytest

from flake8_import_order import STDLIB_NAMES
from flake8_import_order.checker import ImportOrderChecker


def _load_test_cases():
    test_cases = []
    for name in STDLIB_NAMES:
        if not name.startswith("__"):
            test_cases.append(name)
    return test_cases


def _checker(data):
    pycodestyle.stdin_get_value = lambda: data
    tree = ast.parse(data)
    checker = ImportOrderChecker(None, tree)
    checker.options = {}
    return checker


@pytest.mark.parametrize('import_name', _load_test_cases())
def test_styles(import_name):
    data = "import {}\nimport zlib\n".format(import_name)
    checker = _checker(data)
    codes = [error.code for error in checker.check_order()]
    assert codes == []

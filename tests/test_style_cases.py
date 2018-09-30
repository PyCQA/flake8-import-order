import ast
import glob
import os
import re
import sys

import pytest

from flake8_import_order.checker import ImportOrderChecker
from flake8_import_order.styles import lookup_entry_point

ERROR_RX = re.compile("# ((I[0-9]{3} ?)+) ?.*$")


def _extract_expected_errors(data):
    lines = data.splitlines()
    expected_codes = []
    for line in lines:
        match = ERROR_RX.search(line)
        if match is not None:
            codes = match.group(1).split()
            expected_codes.extend(codes)
    return expected_codes


def _load_test_cases():
    base_path = os.path.dirname(__file__)
    test_cases = []
    test_case_path = os.path.join(base_path, 'test_cases')
    wildcard_path = os.path.join(test_case_path, '*.py')

    for filename in glob.glob(wildcard_path):
        # The namespace.py test only works with Python3
        if filename.endswith('namespace.py') and sys.version_info.major < 3:
            continue
        fullpath = os.path.join(test_case_path, filename)
        with open(fullpath) as file_:
            data = file_.read()
        styles = data.splitlines()[0].lstrip('#').strip().split()
        codes = _extract_expected_errors(data)
        tree = ast.parse(data, fullpath)
        for style_name in styles:
            style_entry_point = lookup_entry_point(style_name)
            test_cases.append((filename, tree, style_entry_point, codes))

    return test_cases


def _checker(filename, tree, style_entry_point):
    options = {
        'application_import_names': [
            'flake8_import_order', 'namespace.package_b', 'tests',
        ],
        'application_package_names': ['localpackage'],
        'import_order_style': style_entry_point,
    }
    checker = ImportOrderChecker(filename, tree)
    checker.options = options
    return checker


@pytest.mark.parametrize(
    'filename, tree, style, expected_codes',
    _load_test_cases(),
)
def test_styles(filename, tree, style, expected_codes):
    checker = _checker(filename, tree, style)
    codes = [error.code for error in checker.check_order()]
    assert codes == expected_codes


def test_unknown_style():
    with pytest.raises(LookupError):
        lookup_entry_point('Unknown')

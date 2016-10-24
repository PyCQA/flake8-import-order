import ast
import glob
import os
import re

import pytest

from flake8_import_order.checker import ImportOrderChecker

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
        fullpath = os.path.join(test_case_path, filename)
        with open(fullpath) as file_:
            data = file_.read()
        styles = data.splitlines()[0].lstrip('#').strip().split()
        codes = _extract_expected_errors(data)
        tree = ast.parse(data, fullpath)
        for style in styles:
            test_cases.append((filename, tree, style, codes))

    return test_cases


def _checker(filename, tree, style):
    options = {
        'application_import_names': ['flake8_import_order', 'tests'],
        'import_order_style': style,
    }
    if style == 'appnexus':
        options['application_package_names'] = ['localpackage']
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

import ast
import os

import pytest

from flake8_import_order import pylama_linter

from tests.utils import extract_expected_errors


def load_test_cases():
    base_path = os.path.dirname(__file__)
    test_case_path = os.path.join(base_path, "test_cases")
    test_case_files = os.listdir(test_case_path)

    test_cases = []

    for fname in test_case_files:
        if not fname.endswith(".py"):
            continue

        fullpath = os.path.join(test_case_path, fname)
        data = open(fullpath).read()
        expected = extract_expected_errors(data)

        test_cases.append((fullpath, expected))

    return test_cases


@pytest.mark.parametrize(
    "filename, expected",
    load_test_cases()
)
def test_expected_error(filename, expected):
    checker = pylama_linter.Linter()
    assert checker.allow(filename)

    errors = []
    options = {'import_order_style': 'google'} if 'google' in filename else {}
    for error in checker.run(filename, **options):
        code = error['type']
        errors.append(code)
    assert errors == expected

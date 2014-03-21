import ast
import os

import pytest

from flake8_import_order import flake8_linter


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
        tree = ast.parse(data, fullpath)

        lines = data.splitlines()

        expected = [
            line.split()[1]
            for line in lines
            if line.startswith("# ")
        ]

        test_cases.append((tree, fullpath, expected))

    return test_cases


@pytest.mark.parametrize(
    "tree, filename, expected",
    load_test_cases()
)
def test_expected_error(tree, filename, expected):
    checker = flake8_linter.Linter(
        tree, filename)
    errors = []
    for lineno, col_offset, msg, instance in checker.run():
        errors.append(msg.split()[0])
    assert errors == expected

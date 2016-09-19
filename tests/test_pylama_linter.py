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
        codes, messages = extract_expected_errors(data)

        test_cases.append((fullpath, codes, messages))

    return test_cases


@pytest.mark.parametrize(
    "filename, expected_codes, expected_messages",
    load_test_cases()
)
def test_expected_error(filename, expected_codes, expected_messages):
    checker = pylama_linter.Linter()
    assert checker.allow(filename)

    codes = []
    messages = []

    options = {
        "application_import_names": ["flake8_import_order", "tests"],
        "application_package_names": ["local_package"],
    }

    for style in ['google', 'smarkets', 'pep8']:
        if style in filename:
            options['import_order_style'] = style
            break

    for error in checker.run(filename, **options):
        codes.append(error['type'])
        messages.append(error['text'])

    assert codes == expected_codes
    assert set(messages) >= set(expected_messages)

import pytest


@pytest.mark.skip("pylama seems unmaintained")
def test_linter(tmpdir):
    from flake8_import_order.pylama_linter import Linter

    file_ = tmpdir.join("flake8_import_order.py")
    file_.write("import ast\nimport flake8_import_order\n")

    options = {
        "application-import-names": ["flake8_import_order"],
    }
    checker = Linter()
    assert checker.allow(str(file_))
    for error in checker.run(str(file_), **options):
        assert error["type"] == "I201"

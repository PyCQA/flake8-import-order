from os.path import dirname

from flake8_import_order.pylama_linter import Linter


def test_application_paths():
    import_names = {'flake8_import_order', 'tests', 'setup'}
    path = dirname(dirname(__file__))
    meta = {'application_paths': [path]}
    options = Linter.parse_meta(meta)
    assert set(options['application_import_names']) == import_names


def test_linter(tmpdir):
    file_ = tmpdir.join('flake8_import_order.py')
    file_.write('import ast\nimport flake8_import_order\n')

    options = {
        'application-import-names': ['flake8_import_order'],
    }
    checker = Linter()
    assert checker.allow(str(file_))
    for error in checker.run(str(file_), **options):
        assert error['type'] == 'I201'

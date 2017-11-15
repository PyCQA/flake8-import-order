from collections import namedtuple

from pkg_resources import iter_entry_points

from flake8_import_order import (
    ClassifiedImport, IMPORT_3RD_PARTY, IMPORT_APP, IMPORT_APP_RELATIVE,
    NewLine,
)

Error = namedtuple('Error', ['lineno', 'code', 'message'])


def list_entry_points():
    return iter_entry_points('flake8_import_order.styles')


def lookup_entry_point(name):
    try:
        return next(iter_entry_points('flake8_import_order.styles', name=name))
    except StopIteration:
        raise LookupError('Unknown style {}'.format(name))


class Style(object):

    accepts_application_package_names = False

    def __init__(self, nodes):
        self.nodes = nodes

    def check(self):
        previous = None
        previous_import = None
        for current in self.nodes:
            if isinstance(current, ClassifiedImport):
                for error in self._check(previous_import, previous, current):
                    yield error
                previous_import = current
            previous = current

    def _check(self, previous_import, previous, current_import):
        if current_import.type == -1:
            yield Error(
                current_import.lineno,
                'I666',
                'Import statement mixes groups',
            )

        correct_names = self.sorted_names(current_import.names)
        if correct_names != current_import.names:
            corrected = ', '.join(correct_names)
            yield Error(
                current_import.lineno,
                'I101',
                "Imported names are in the wrong order. "
                "Should be {0}".format(corrected),
            )

        if previous_import is not None:
            previous_key = self.import_key(previous_import)
            current_key = self.import_key(current_import)
            if previous_key > current_key:
                first = self._explain(current_import)
                second = self._explain(previous_import)
                if first == second:
                    first = ", ".join(current_import.names)
                    second = ", ".join(previous_import.names)
                yield Error(
                    current_import.lineno,
                    'I100',
                    "Import statements are in the wrong order. "
                    "{0} should be before {1}".format(first, second),
                )

            same_section = self.same_section(previous_import, current_import)
            has_newline = isinstance(previous, NewLine)
            if not same_section and not has_newline:
                yield Error(
                    current_import.lineno,
                    'I201',
                    'Missing newline before sections or imports.',
                )

            if same_section and has_newline:
                yield Error(
                    current_import.lineno,
                    'I202',
                    'Additional newline in a section of imports.',
                )

    @staticmethod
    def sorted_names(names):
        return names

    @staticmethod
    def import_key(import_):
        return (import_.type,)

    @staticmethod
    def same_section(previous, current):
        same_type = current.type == previous.type
        both_first = (
            {previous.type, current.type} <= {IMPORT_APP, IMPORT_APP_RELATIVE}
        )
        return same_type or both_first

    @staticmethod
    def _explain(import_):
        if import_.is_from:
            text = 'from ' + import_.level * '.'
        else:
            text = 'import '
        return text + ', '.join(import_.modules)


class PEP8(Style):
    pass


class Google(Style):

    @staticmethod
    def sorted_names(names):
        return sorted(names, key=Google.name_key)

    @staticmethod
    def name_key(name):
        return (name.lower(), name)

    @staticmethod
    def import_key(import_):
        modules = [Google.name_key(module) for module in import_.modules]
        names = [Google.name_key(name) for name in import_.names]
        return (import_.type, import_.level, modules, names)


class AppNexus(Google):
    accepts_application_package_names = True


class Smarkets(Style):

    @staticmethod
    def sorted_names(names):
        return sorted(names, key=Smarkets.name_key)

    @staticmethod
    def name_key(name):
        return (name.lower(), name)

    @staticmethod
    def import_key(import_):
        modules = [Smarkets.name_key(module) for module in import_.modules]
        names = [Smarkets.name_key(name) for name in import_.names]
        return (import_.type, import_.is_from, import_.level, modules, names)


class Edited(Smarkets):
    accepts_application_package_names = True


class Cryptography(Style):

    @staticmethod
    def sorted_names(names):
        return sorted(names)

    @staticmethod
    def import_key(import_):
        if import_.type in {IMPORT_3RD_PARTY, IMPORT_APP}:
            return (
                import_.type, import_.package, import_.is_from,
                import_.level, import_.modules, import_.names,
            )
        else:
            return (
                import_.type, '', import_.is_from, import_.level,
                import_.modules, import_.names,
            )

    @staticmethod
    def same_section(previous, current):
        app_or_third = current.type in {IMPORT_3RD_PARTY, IMPORT_APP}
        same_type = current.type == previous.type
        both_relative = previous.type == current.type == IMPORT_APP_RELATIVE
        same_package = previous.package == current.package
        return (
            (not app_or_third and same_type or both_relative) or
            (app_or_third and same_package)
        )

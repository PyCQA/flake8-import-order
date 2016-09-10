from collections import namedtuple

from flake8_import_order import (
    IMPORT_3RD_PARTY, IMPORT_APP, IMPORT_APP_RELATIVE,
)

RELATIVE_SET = {IMPORT_APP, IMPORT_APP_RELATIVE}

Error = namedtuple('Error', ['lineno', 'code', 'message'])


class Style(object):

    def __init__(self, imports):
        self.imports = imports

    def check(self):
        previous = None
        for current in self.imports:
            if current.type == -1:
                yield Error(
                    current.lineno,
                    'I666',
                    'Import statement mixes groups',
                )

            correct_names = self.sorted_names(current.names)
            if correct_names != current.names:
                corrected = ', '.join(correct_names)
                yield Error(
                    current.lineno,
                    'I101',
                    "Imported names are in the wrong order. "
                    "Should be {0}".format(corrected),
                )

            if previous is not None:
                if self.key(previous) > self.key(current):
                    first = self._explain(current)
                    second = self._explain(previous)
                    yield Error(
                        current.lineno,
                        'I100',
                        "Import statements are in the wrong order. "
                        "{0} should be before {1}".format(first, second),
                    )

                spacing = current.lineno - previous.lineno
                if not self.same_section(previous, current) and spacing == 1:
                    yield Error(
                        current.lineno,
                        'I201',
                        'Missing newline before sections or imports.',
                    )

            previous = current

    @staticmethod
    def sorted_names(names):
        return names

    @staticmethod
    def key(import_):
        return (import_.type,)

    @staticmethod
    def same_section(previous, current):
        same_type = current.type == previous.type
        both_relative = {previous.type, current.type} <= RELATIVE_SET
        return same_type or both_relative

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
        return sorted(names, key=lambda n: n.lower())

    @staticmethod
    def key(import_):
        modules = [module.lower() for module in import_.modules]
        return (import_.type, import_.level, modules, import_.names)


class AppNexus(Google):
    pass


class Smarkets(Style):

    @staticmethod
    def sorted_names(names):
        return sorted(names, key=lambda n: n.lower())

    @staticmethod
    def key(import_):
        modules = [module.lower() for module in import_.modules]
        return (
            import_.type, import_.is_from, import_.level, modules,
            import_.names,
        )


class Cryptography(Style):

    @staticmethod
    def sorted_names(names):
        return sorted(names)

    @staticmethod
    def key(import_):
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
        both_relative = {previous.type, current.type} <= RELATIVE_SET
        same_package = previous.package == current.package
        return (
            (not app_or_third and same_type or both_relative) or
            (app_or_third and same_package)
        )

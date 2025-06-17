import importlib.metadata
from collections import namedtuple

from flake8_import_order import ClassifiedImport
from flake8_import_order import ImportType
from flake8_import_order import NewLine

Error = namedtuple("Error", ["lineno", "code", "message"])


def list_entry_points():
    entry_points = importlib.metadata.entry_points()
    if not hasattr(entry_points, "select"):
        return entry_points.get("flake8_import_order.styles", [])
    return entry_points.select(group="flake8_import_order.styles")


def lookup_entry_point(name):
    for style in list_entry_points():
        if style.name == name:
            return style

    raise LookupError(f"Unknown style {name}")


class Style:

    accepts_application_package_names = False

    def __init__(self, nodes):
        self.nodes = nodes

    def check(self):
        previous = None
        previous_import = None
        for current in self.nodes:
            if isinstance(current, ClassifiedImport):
                yield from self._check(previous_import, previous, current)
                previous_import = current
            previous = current

    def _check(self, previous_import, previous, current_import):
        yield from self._check_I666(current_import)
        yield from self._check_I101(current_import)
        if (
            previous_import is not None
            and not previous_import.type_checking
            and current_import.type_checking
        ):
            yield from self._check_I300(previous_import, current_import)
            previous_import = None
        if previous_import is not None:
            yield from self._check_I100(previous_import, current_import)
            yield from self._check_I201(
                previous_import, previous, current_import
            )
            yield from self._check_I202(
                previous_import, previous, current_import
            )

    def _check_I666(self, current_import):  # noqa: N802
        if current_import.type == ImportType.MIXED:
            yield Error(
                current_import.lineno,
                "I666",
                "Import statement mixes groups",
            )

    def _check_I101(self, current_import):  # noqa: N802
        correct_names = self.sorted_names(current_import.names)
        if correct_names != current_import.names:
            corrected = ", ".join(correct_names)
            yield Error(
                current_import.lineno,
                "I101",
                "Imported names are in the wrong order. "
                "Should be {}".format(corrected),
            )

    def _check_I300(self, previous_import, current_import):  # noqa: N802
        if current_import.lineno - previous_import.end_lineno != 3:
            yield Error(
                current_import.lineno,
                "I300",
                "TYPE_CHECKING block should have one newline above.",
            )

    def _check_I100(self, previous_import, current_import):  # noqa: N802
        previous_key = self.import_key(previous_import)
        current_key = self.import_key(current_import)
        if previous_key > current_key:
            message = (
                "Import statements are in the wrong order. "
                "'{}' should be before '{}'"
            ).format(
                self._explain_import(current_import),
                self._explain_import(previous_import),
            )
            same_section = self.same_section(
                previous_import,
                current_import,
            )
            if not same_section:
                message = f"{message} and in a different group."
            yield Error(current_import.lineno, "I100", message)

    def _check_I201(  # noqa: N802
        self, previous_import, previous, current_import
    ):
        same_section = self.same_section(previous_import, current_import)
        has_newline = isinstance(previous, NewLine)
        if not same_section and not has_newline:
            yield Error(
                current_import.lineno,
                "I201",
                "Missing newline between import groups. {}".format(
                    self._explain_grouping(
                        current_import,
                        previous_import,
                    )
                ),
            )

    def _check_I202(  # noqa: N802
        self, previous_import, previous, current_import
    ):
        same_section = self.same_section(previous_import, current_import)
        has_newline = isinstance(previous, NewLine)
        if same_section and has_newline:
            yield Error(
                current_import.lineno,
                "I202",
                "Additional newline in a group of imports. {}".format(
                    self._explain_grouping(
                        current_import,
                        previous_import,
                    )
                ),
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
        both_first = {previous.type, current.type} <= {
            ImportType.APPLICATION,
            ImportType.APPLICATION_RELATIVE,
        }
        return same_type or both_first

    @staticmethod
    def _explain_import(import_):
        if import_.is_from:
            return "from {}{} import {}".format(
                import_.level * ".",
                ", ".join(import_.modules),
                ", ".join(import_.names),
            )
        else:
            return "import {}".format(", ".join(import_.modules))

    @staticmethod
    def _explain_grouping(current_import, previous_import):
        return (
            "'{}' is identified as {} and " "'{}' is identified as {}."
        ).format(
            Style._explain_import(current_import),
            current_import.type.name.title().replace("_", " "),
            Style._explain_import(previous_import),
            previous_import.type.name.title().replace("_", " "),
        )


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

    def _check_I202(  # noqa: N802
        self, previous_import, previous, current_import
    ):
        same_section = self.same_section(previous_import, current_import)
        has_newline = isinstance(previous, NewLine)
        optional_split = (
            current_import.is_from and not previous_import.is_from
        )
        if same_section and has_newline and not optional_split:
            yield Error(
                current_import.lineno,
                "I202",
                "Additional newline in a group of imports. {}".format(
                    self._explain_grouping(
                        current_import,
                        previous_import,
                    )
                ),
            )

    @staticmethod
    def same_section(previous, current):
        return current.type == previous.type


class PyCharm(Smarkets):
    @staticmethod
    def sorted_names(names):
        return sorted(names)

    @staticmethod
    def import_key(import_):
        return (
            import_.type,
            import_.is_from,
            import_.level,
            import_.modules,
            import_.names,
        )


class ISort(PyCharm):
    @staticmethod
    def name_key(name):
        # Group by CONSTANT, Class, func.
        group = 0 if name.isupper() else 2 if name.islower() else 1
        return (group, name)

    @staticmethod
    def sorted_names(names):
        return sorted(names, key=ISort.name_key)


class Cryptography(Style):

    @staticmethod
    def sorted_names(names):
        return sorted(names)

    @staticmethod
    def import_key(import_):
        if import_.type in {ImportType.THIRD_PARTY, ImportType.APPLICATION}:
            return (
                import_.type,
                import_.package,
                import_.is_from,
                import_.level,
                import_.modules,
                import_.names,
            )
        else:
            return (
                import_.type,
                "",
                import_.is_from,
                import_.level,
                import_.modules,
                import_.names,
            )

    @staticmethod
    def same_section(previous, current):
        app_or_third = current.type in {
            ImportType.THIRD_PARTY,
            ImportType.APPLICATION,
        }
        same_type = current.type == previous.type
        both_relative = (
            previous.type == current.type == ImportType.APPLICATION_RELATIVE
        )
        same_package = previous.package == current.package
        return (not app_or_third and same_type or both_relative) or (
            app_or_third and same_package
        )

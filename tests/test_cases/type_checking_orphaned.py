# cryptography edited google pep8 smarkets
from typing import TYPE_CHECKING

import pytest

from . import localpackage

CONST = localpackage.CONST

if TYPE_CHECKING:
    import ast  # I301

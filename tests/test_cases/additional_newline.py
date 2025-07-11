# appnexus google pep8 smarkets
import ast
# This comment should not trigger a I202 (not a newline)
import os

import signal # I202

import X
from X import B, b, \
    C, d

from Y import A # I202
from Y import (
    B, b,
    C, d,
)
from Z import A

import flake8_import_order

import tests  # I202
from . import A

from . import B  # I202
from .Z import (
    A,
    B,
    C,
    D,
    E,
    F,
    G,
)

if TYPE_CHECKING:
    import ast
    # This comment should not trigger a I202 (not a newline)
    import os

    import signal # I202

    import X
    from X import B, b, \
        C, d

    from Y import A # I202
    from Y import (
        B, b,
        C, d,
    )
    from Z import A

    import flake8_import_order

    import tests  # I202
    from . import A

    from . import B  # I202

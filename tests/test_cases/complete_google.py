from __future__ import absolute_import

import ast
import os
import sys
from functools import *
from os import path

import flake8_import_error
import X
import Y
import Z
from flake8_import_error import *
from X import *
from X import A
from X import b, C, d
from Y import *
from Y import A
from Y import B, C, D
from Z import A
from Z.A import A
from Z.A.B import A

from . import A
from . import B
from .. import A
from .. import B

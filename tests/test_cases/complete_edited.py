# edited
from __future__ import absolute_import

import ast
import os
import StringIO
import sys
from functools import *
from os import path

import X
import Y
import Z
from X import *
from X import A
from X import B, b, C, d
from Y import *
from Y import A
from Y import B, C, D
from Y import e
from Z import A
from Z.A import A
from Z.A.B import A

import localpackage

from localpackage import A, b

import flake8_import_order
from flake8_import_order import *

from . import A
from . import B
from .A import A
from .B import B
from .. import A
from .. import B
from ..A import A
from ..B import B

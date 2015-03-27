from __future__ import absolute_import

import ast
import os
import sys
from functools import *
from os import path

import X
from X import *
from X import A
from X import B, C, D

import Y
from Y import *
from Y import A
from Y import B, C, D

import Z
from Z import A
from Z.A import A
from Z.A.B import A

import flake8_import_order
from flake8_import_order import *
from flake8_import_order import A
from flake8_import_order import B

import tests
from tests import A
from tests import B

from . import A
from . import B
from .A import A
from .B import B
from .. import A
from .. import B
from ..A import A
from ..B import B

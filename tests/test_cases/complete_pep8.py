from __future__ import absolute_import

import sys
from os import path
import os
from functools import *
import ast

import X
from X import *
from X import b
from X import A, C, d
import Z
from Z import A
from Z.A import A
from Z.A.B import A
import Y
from Y import *
from Y import B
from Y import A, C, D

import flake8_import_order
from flake8_import_order import *
from . import B
from . import A
from .B import B
from .A import A
from .. import B
from .. import A
from ..B import B
from ..A import A

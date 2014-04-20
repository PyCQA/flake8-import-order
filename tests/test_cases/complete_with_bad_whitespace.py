from __future__ import absolute_import

import ast
import os

import sys

from functools import *

from os import path
import X # I201
from X import *
from X import A

from X import B, C, D
import Y # I201
from Y import *
from Y import A
from Y import B, C, D
import flake8_import_error # I201

from flake8_import_error import *

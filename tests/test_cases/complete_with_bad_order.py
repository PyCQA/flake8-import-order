from __future__ import absolute_import

import ast
import sys
import os # I100
from os import path
from functools import * # I100

from X import *
import X # I100
from X import A
from X import B, C, D

import Y
from Y import *
from Y import A
from Y import B, D, C # I101

from Z import A
from Z.A.B import A
from Z.A import A # I100

import flake8_import_error
from flake8_import_error import *


import ast
import os
import sys
from functools import *
from os import path

from __future__ import absolute_import # I100

import X
from X import *
from X import A
from X import B, C, D

import flake8_import_error # I100
from flake8_import_error import *

from Y import *
import Y # I100
from Y import A
from Y import B, C, D

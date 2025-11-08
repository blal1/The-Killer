"""
mathutils — Math and RNG mapping.
"""
from __future__ import annotations
import math
import random

# Direct maps
absolute = abs
floor = math.floor
ceiling = math.ceil
power = pow
log = math.log
log10 = math.log10
cosine = math.cos
arc_cosine = math.acos
arc_sine = math.asin
arc_tangent = math.atan
exponent = math.exp

def random_int(a, b):
    return random.randint(a, b)

def random_float(a=0.0, b=1.0):
    return random.uniform(a, b)

def random_get_state():
    return random.getstate()

def random_set_state(state):
    return random.setstate(state)

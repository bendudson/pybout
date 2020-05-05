"""
Example
-------

import pybout

f = pybout.Field("f")
g = pybout.Field("g")

f.ddt = g
g.ddt = -f

model = pybout.PhysicsModel(f, g)

print(str(model))  # Generates C++ code
"""


from .fieldexpr import Field

from .functions import Delp2

from .physicsmodel import PhysicsModel

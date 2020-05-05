"""
Define functions which can operate on FieldExpr objects, and be
translated into BOUT++ function calls.

These should handle:

 - Calling on fields or at an index, if possible
 - Deciding if communications are needed 
 - The include files needed
"""

from .fieldexpr import FieldExprOp, makeFieldExpr

class BoutFunction(FieldExprOp):

    name = None     # Function name
    include = None   # Required include file
    single_index = False  # Can be used as single index?
    
    def __init__(self, name, *args, include=None, single_index=False):
        self.name = name
        self.include = include
        self.single_index = single_index
        self.args = map(makeFieldExpr, args)

    def __repr__(self):
        result = "BoutFunction('" + self.name + "'"
        if self.args:
            result += ", " + ", ".join(map(repr, self.args))
        if self.include:
            result += ", include=" + repr(self.include)
        return result + ")"
    
    def asBoutReal(self, index):
        assert self.single_index
        return (self.name +
                "(" +
                ", ".join([arg.asField() for arg in self.args]) +
                ", " + str(index) + 
                ")")

    def asField(self):
        return (self.name +
                "(" +
                ", ".join([arg.asField() for arg in self.args]) +
                ")")

Delp2 = lambda f: BoutFunction("Delp2", f, include="difops.hxx", single_index=True)


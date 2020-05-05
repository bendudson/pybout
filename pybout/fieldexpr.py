"""
Define the base class which represents values and expressions

FieldExpr          Base class
  - Field          Field3D object, calculated in C++ code
  - KnownScalar    Scalar value (int/float) known at compile time

makeField(value) :: value -> FieldExpr 
            A function to turn a value into a FieldExpr

"""

class FieldExpr:
    """
    Base class for all expressions which can be evaluated at any point in 3D
    
    This includes Field3D objects, but can also include complex expressions
    
    """

    def asBoutReal(self, index):
        """Return a string (C++) which will evaluate the expression
        at the given index, i.e. as a BoutReal
        """
        raise ValueError("FieldExpr.asBoutReal not implemented")

    def asField(self):
        """Return a string (C++) which will evaluate the expression
        as a Field3D
        """
        raise ValueError("FieldExpr.asField not implemented")
    
    # Unary -
    def __neg__(self):
        return BinOp(self, KnownScalar(-1), "*")
    
    # Operations where the FieldExpr is on the left
    
    def __add__(self, other):
        return BinOp(self, other, "+")
    
    def __sub__(self, other):
        return BinOp(self, other, "-")
    
    def __mul__(self, other):
        return BinOp(self, other, "*")

    def __div__(self, other):
        return BinOp(self, other, "/")

    # Operations where the FieldExpr is on the right
    
    def __radd__(self, other):
        return BinOp(other, self, "+")
    
    def __rsub__(self, other):
        return BinOp(other, self, "-")
    
    def __rmul__(self, other):
        return BinOp(other, self, "*")

    def __rdiv__(self, other):
        return BinOp(other, self, "/")

class Field(FieldExpr):
    """A Field3D object calculated at runtime
    """
    
    name = "unknown";
    def __init__(self, name):
        """A Field3D object. The given name will be used in the C++ code.
        """
        self.name = name
    
    def asBoutReal(self, index):
        return self.name + "[" + str(index) + "]"

    def asField(self):
        return self.name

    def __repr__(self):
        return "Field('" + self.name + "')"

class KnownScalar(FieldExpr):
    """Scalar value known at compile time
    """
    def __init__(self, value):
        self.value = value
        
    def asBoutReal(self, index):
        return str(self.value)

    def asField(self):
        return str(self.value)

def makeFieldExpr(value):
    """Convert a value to a FieldExpr instance. If the input is
    already an instance, it is passed through.
    """
    if isinstance(value, FieldExpr):
        return value
    # Try to convert to int or float
    try:
        return KnownScalar(int(value))
    except ValueError:
        pass
    return KnownScalar(float(value))


class FieldExprOp(FieldExpr):
    """A field expression which involves operation(s) on other FieldExpr objects
    """
    args = []  # List of arguments

class BinOp(FieldExprOp):
    """Binary operation e.g. +,-,*,/
    """
    def __init__(self, left, right, op):
        self.args = [makeFieldExpr(left), makeFieldExpr(right)]
        self.op = op
        
    def asBoutReal(self, index):
        return "(" + self.args[0].asBoutReal(index) + self.op + self.args[1].asBoutReal(index) + ")"
    
    def asField(self):
        return "(" + self.args[0].asField() + self.op + self.args[1].asField() + ")"

    def __repr__(self):
        return "(" + repr(self.args[0]) + self.op + repr(self.args[1]) + ")"
    
    def __str__(self):
        return "(" + str(self.args[0]) + self.op + str(self.args[1]) + ")"

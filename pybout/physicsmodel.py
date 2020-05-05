"""
Top level structures and code generation

"""


class BlockScope:
    """
    Define a block of code which has specified inputs and calculates
    a number of outputs.
    """
    def __init__(self, inputs=None, assigns=None):
        """
        Inputs
        ------

        inputs     A list of Field objects
        assigns    A list of tuples ("name", FieldExpr)
        """
        self.inputs = inputs
        self.assigns = assigns

    def __str__(self):
        """
        Generate the C++ code for this block
        """
        return "\n".join([name + " = " + expr.asField() + ";"
                          for name, expr in self.assigns])

class PhysicsModel:
    """
    Defines the physics model, which will be translated to C++ 
    """
    def __init__(self, *variables):
        """
        Inputs
        ------

        variables    Field objects. Their ddt attributes should contain
                     FieldExpr objects which define how they are calculated
        """
        self._evolving_variables = variables
        self.rhs_function = BlockScope(inputs = variables,
                                       assigns = [("ddt(" + var.name + ")",
                                                   var.ddt)
                                                  for var in variables])
    
    def evolvingVariables(self):
        return self._evolving_variables
    
    def rhsFunction(self):
        return self.rhs_function

    def __str__(self):
        header_files = ["bout/physicsmodel.hxx"]
        
        return """
        {header}
        
        class Model : public PhysicsModel {{
        private:
          // Evolving fields
          {defines}
        
        protected:
          int init(bool restarting) override {{
        
            // Evolving quantities
            {solve_fors}
            return 0;
          }}
        
          int rhs(BoutReal time) override {{
            {rhs_function}
            return 0;
          }}
        }};

        BOUTMAIN(Model);
        """.format(header = "\n".join(["#include \"" + filename + "\""
                                       for filename in header_files]),
                   
                   defines = "\n".join(["Field3D " + var.name + ";"
                                        for var in self.evolvingVariables()]),
                   
                   solve_fors = "\n".join(["SOLVE_FOR(" + var.name + ");"
                                           for var in self.evolvingVariables()]),
                   
                   rhs_function = str(self.rhsFunction()))

    

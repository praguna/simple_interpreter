# DEFINED TO PROVIDE INTERFACE FOR VISITOR NODES

class NodeVisitor():
    def visit(self,node):
        method_name = 'visit_'+type(node).__name__
        visitor = getattr(self,method_name, 'generic_visit')
        return visitor(node)

    def generic_visit(self,node):
        raise Exception("visit_{} does not exit".format(type(node).__name__))
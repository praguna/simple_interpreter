from token import *
from visitor import NodeVisitor
# EACH FUNCTION STARTING WITH visit_ handles corresponding AST NODE
class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self,tree):
        self.tree =tree
    
    def interpret(self):
        self.visit(self.tree)
    
    def visit_Program(self,program):
        self.visit(program.block)
    
    def visit_Block(self,block):
        for declaration in block.declarations:
            self.visit(declaration)
        self.visit(block.compound_statement)
    
    def visit_VarDecl(self,var_decl):
        pass

    def visit_NoOp(self,node):
        pass

    def visit_Num(self,node):
        return node.value
    
    def visit_Assign(self,node):
        self.GLOBAL_SCOPE[node.left.value] = self.visit(node.right)
    
    def visit_Var(self,node):
        val = self.GLOBAL_SCOPE.get(node.value,None)
        if val is None:
            raise NameError("Variable {} not found".format(node.value))
        return val
    
    def visit_UnOp(self,node):
        token  = node.op
        if token.type == Token_Type.PLUS:
            return +self.visit(node.expr)
        elif token.type == Token_Type.MINUS:
            return  -self.visit(node.expr)

    def visit_BnOp(self,node):
        token = node.op
        if token.type == Token_Type.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif token.type == Token_Type.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif token.type == Token_Type.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif token.type == Token_Type.DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif token.type == Token_Type.DIV_FLOAT:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_ProcedureDecl(self,node):
        pass

    def visit_Params(self,node):
        pass
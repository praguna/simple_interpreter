from token import *
from visitor import NodeVisitor

class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self,parser):
        self.parser =parser
    
    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)
        print(self.GLOBAL_SCOPE)
    
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
        if token.type == PLUS:
            return +self.visit(node.expr)
        elif token.type == MINUS:
            return  -self.visit(node.expr)

    def visit_BnOp(self,node):
        token = node.op
        if token.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif token.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif token.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif token.type == DIV_INT:
            return self.visit(node.left) // self.visit(node.right)
        elif token.type == DIV_FLOAT:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

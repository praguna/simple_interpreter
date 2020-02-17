#AST 
class AST():
    pass

class BnOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

class UnOp(AST):
    def __init__(self,op,expr):
        self.op = op
        self.expr = expr

class Program(AST):
    def __init__(self,name,block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self,declarations,compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self,var_node,type_node):
        self.var_node = var_node
        self.type_node = type_node

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

class Compound(AST):
    def __init__(self):
        self.children = []

class NoOp(AST):
    pass

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Type(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value
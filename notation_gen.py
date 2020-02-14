from rewrite_ast_1 import *

class RPNConversion(NodeVisitor):

    def visit_BinOp(self,node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return '{left}{right}{op}'.format(left = left_val, right = right_val, op = node.op.value)

    def visit_Num(self, node):
        return node.value

class LISPConversion(NodeVisitor):
    def visit_BinOp(self,node):
        res = node.op.value
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return res+'{left}{right}'.format(left = left_val, right = right_val)

    def visit_Num(self, node):
        return node.value

class UnitTest():
    def __init__(self, type = "rpn"):
        if type=="rpn" : self.rpn()
        elif type == "lisp": self.lisp()
        

    def  rpn(self):
        values = [('2+3*4','234*+')]
        for x,y in values:
            val = RPNConversion().visit(Parser(Lexer(x)).parse())
            assert(val == y)
        print(" RPN passed !")

    def lisp(self):
        values = [('2+3*4','+2*34')]
        for x,y in values:
            val = LISPConversion().visit(Parser(Lexer(x)).parse())
            assert(val == y)
        print(" LISP passed !")

if __name__ == '__main__':
    UnitTest(type = 'rpn')
    UnitTest(type = 'lisp')
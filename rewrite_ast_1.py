## Simple Calculator Interpreter with AST
## Basic Tokens Allowed
INTEGER,PLUS,MUL,DIV,MINUS,LPARAN,RPARAN,EOF = (
    'INTEGER','PLUS','MUL','DIV','MINUS','LPARAN','RPARAN','EOF'
)
#Token Class = Defines Tokens
class Token(object):
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'TOKEN({type},{value})'.format(type = self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

#LEXER or Scanner Class - Checks validity of characters and generates tokens
class Lexer(object):
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid Character")

    def advance(self):
        self.pos+=1
        if self.pos > len(self.text) - 1:
             self.current_char = None
        else: 
            self.current_char = self.text[self.pos] 

    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER,self.get_integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS , '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL , '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV , '/')     
            if self.current_char == '(':
                self.advance()
                return Token(LPARAN , '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPARAN , ')')
            self.error()
        return Token(EOF,None)

#Parser  - Checks Syntax of the Expression and generates IR
class AST(object):
    pass

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.op = self.token = op
        self.right = right

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class UnOp(AST):
    def __init__(self,op,expr):
        self.token = self.op = op
        self.expr = expr

class Parser(object):
    def __init__(self,lexer):
        self.lexer  = lexer
        self.current_token = lexer.next_token()
    def error(self):
        raise Exception("Invalid Syntax")
    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            self.error()

    def factor(self):
        """
        f : (PLUS|MINUS)f | INTEGER | LPARAN E RPARAN
        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        if token.type == LPARAN:
            self.eat(LPARAN)
            node = self.expr()
            self.eat(RPARAN)
            return node
        if token.type == PLUS:
            self.eat(PLUS) 
            node = UnOp(op = token, expr = self.factor())
            return node 
        if token.type == MINUS:
            self.eat(MINUS)
            node = UnOp(op = token, expr = self.factor())
            return node

    def term(self):
        """
        T : f((MUL|DIV)f)*
        """
        node  = self.factor()
        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == PLUS:
                self.eat(PLUS)
            node  = BinOp(left = node, op = token, right= self.factor())
        return node

    def expr(self):
        """
        E : T((PLUS|MINUS)T)*
        """
        node = self.term()
        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left = node, op = token ,right = self.term())
        return node

    def parse(self):
        result = self.expr()
        if self.current_token.type is not EOF: 
            self.error()
        return result

class NodeVisitor(object):
    def visit(self,node):
        method_name = 'visit_'+type(node).__name__
        self.visitor = getattr(self,method_name,self.generic_visit)
        return self.visitor(node)

    def generic_visit(self,node):
        raise Exception("No visit_{} method".format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self,parser):
        self.parser = parser
    
    def visit_BinOp(self,node):
        if node.op.type == PLUS:
           return self.visit(node.left) + self.visit(node.right)
        if node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self,node):
        return node.value

    def visit_UnOp(self,node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        if op == MINUS:
            return -self.visit(node.expr)
    
    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

if __name__ == '__main__':
    while(True):
        try:
            text = input("rewrite_ast_1 >")
        except EOFError:  break
        if not text: continue
        if text == "bye": break
        intrepreter = Interpreter(Parser(Lexer(text)))
        print(intrepreter.interpret())
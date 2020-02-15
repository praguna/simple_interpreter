#Token types
(MINUS,PLUS,INTEGER,SEMI,DOT,LPARAN,RPARAN,END,BEGIN,MUL,DIV,ID,EOF,ASSIGN) =(
    "MINUS","PLUS","INTEGER","SEMI","DOT","LPAREN","RPAREN","END","BEGIN","MUL","DIV","ID","EOF","ASSIGN"
)
#Token Class
class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return 'TOKEN({type},{value})'.format(type = self.type, value = self.value)
    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {"END" : Token(END,END), "BEGIN" : Token(BEGIN,BEGIN), "DIV" : Token(DIV,DIV)}

class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def peek(self):
        pos = self.pos + 1
        if pos > len(self.text) - 1:
            return None
        return self.text[pos]

    def advance(self):
        self.pos+=1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else : 
            self.current_char = self.text[self.pos]

    def get_integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        result = ''
        if self.current_char == '_': 
            result = '_'
            self.advance()
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result.upper(),Token(ID,result))
        return token

    def error(self):
        raise Exception("Invalid Character!")

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
                continue
            if self.current_char.isdigit():
                  return Token(INTEGER,self.get_integer())
            if self.current_char == '(':
                self.advance()
                return Token(LPARAN,'(')
            if self.current_char == ')':
                self.advance()
                return Token(RPARAN,')')
            if self.current_char == '*':
                self.advance()
                return Token(MUL,'*')
            # if self.current_char == '/':
            #     self.advance()    # for the sake of excercise 
            #     return Token(DIV,'/')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS,'-')
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN,':=')
            if self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            if self.current_char.isalpha() or (self.current_char == '_' and self.peek().isalpha()):
                return self._id()
            if self.current_char == ';':
                self.advance()
                return Token(SEMI,';')
            if self.current_char == '.':
                self.advance()
                return Token(DOT,'.')
            self.error()
        return Token(EOF,None)

#DEFINE AST Nodes
class AST():
    pass

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left =left
        self.token = self.op = op
        self.right =right

class UnOp(AST):
    def __init__(self,op,expr):
        self.expr =  expr
        self.token = op 

class NUM(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class ASSGN(AST):
    def __init__(self,left,op,expr):
        self.left = left
        self.op = op
        self.expr = expr

class VAR(AST):
    def __init__(self,token):
        self.token = token
        self.value =token.value

class Compound(AST):
    def __init__(self):
        self.children = []
#Parser
class Parser():
    def __init__(self,lexer:Lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()

    def error(self):
        raise Exception("Invalid Syntax!")

    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token  = lexer.next_token()
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL,DIV):
            token =  self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(node,token,self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == MINUS:
                self.eat(MINUS)
            elif token.type == PLUS:
                self.eat(PLUS)
            node = BinOp(node,token,self.term())
        return node

    def variable(self):
        token = self.current_token
        self.eat(ID)
        return VAR(token)

    def empty(self):
        return NoOp()
    
    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return ASSGN(left,token,right)

    def statement(self):
        if self.current_token.type == BEGIN:
            node =  self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        token = Compound()
        token.children = nodes
        return token

    def statement_list(self):
        nodes = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            nodes.append(self.statement())
        if self.current_token.type == ID:
            self.error()
        return nodes
    
    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnOp(token,self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnOp(token,self.factor())
        elif token.type == LPARAN:
            self.eat(LPARAN)
            node = self.expr()
            self.eat(RPARAN)
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return NUM(token)
        else:
            return self.variable()


    def program(self):
        node = self.compound_statement()
        self.eat(DOT)
        return node
    
    def parse(self):
        node = self.program()
        if self.current_token.type is not EOF:
            self.error()
        return node

#Interpreter
class NodeVisitor():
    def visit(self,node):
        method_name = 'visit_'+type(node).__name__
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)

    def generic_visit(self,node):
        raise Exception("No visit_{} found".format(type(node).__name__))

class Interpreter(NodeVisitor):
    SYM_TABLE = {}

    def __init__(self,parser:Parser):
        self.parser = parser
    
    def visit_BinOp(self,node):
        token = node.op
        if token.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if token.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if token.type == DIV:
            return self.visit(node.left) // self.visit(node.right)
        if token.type == MUL:
            return self.visit(node.left) * self.visit(node.right)    

    def visit_Compound(self,node):
        for child in node.children:
            self.visit(child)

    def visit_UnOp(self,node):
        op  = node.token.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_ASSGN(self,node):
        var_name = node.left.value.upper()
        val = self.visit(node.expr)
        self.SYM_TABLE[var_name] = val

    def visit_NUM(self,node:NUM):
        return node.value

    def visit_VAR(self,node):
        var_name = node.value.upper()
        val = self.SYM_TABLE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_NoOp(self,node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)
        print(self.SYM_TABLE)
    

if __name__ == "__main__":
    import sys
    text = open(sys.argv[1],"r+").read()
    lexer = Lexer(text)
    # while lexer.current_char is not None:
    #     print(lexer.next_token())
    parser  = Parser(lexer)
    Interpreter(parser).interpret()
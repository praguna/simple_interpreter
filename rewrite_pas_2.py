# TOKEN
PROGRAM,INTEGER,REAL,PLUS,MINUS,DIV_INT,DIV_FLOAT,SEMI,COLON,ASSGN,LPAREN,MUL,RPAREN,EOF,DOT,ID,BEGIN,END,VAR,INT_CONST,FLOAT_CONST,COMMA =(
    "PROGRAM","INTEGER","REAL","PLUS","MINUS","DIV_INT","DIV_FLOAT","SEMI","COLON","ASSGN","LPAREN","MUL",
    "RPAREN","EOF","DOT","ID","BEGIN","END","VAR","INT_CONST","FLOAT_CONST","COMMA"
)
# TOKEN CLASS
class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return "TOKEN({type},{value})".format(type = self.type,value = self.value)
    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    "BEGIN": Token(BEGIN,BEGIN),
    "END" : Token(END,END),
    "VAR" : Token(VAR, VAR),
    "PROGRAM" : Token(PROGRAM,PROGRAM),
    "DIV" : Token(DIV_INT,DIV_INT),
    "INTEGER" : Token(INTEGER,INTEGER),
    "REAL": Token(REAL,REAL)
}
# LEXER CLASS
class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def advance(self):
        self.pos+=1
        if self.pos > len(self.text) -1:
            self.current_char = None
        else : self.current_char = self.text[self.pos]

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
                continue
            if self.current_char == '{':
                self.skip_comment()
                continue
            if self.current_char.isalpha() or (self.current_char == '_' and self.peek().isalpha()):
                return self._id() 
            if self.current_char == ';':
                self.advance()
                return Token(SEMI,';')
            if self.current_char == '.':
                self.advance()
                return Token(DOT,'.')
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN,'(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN,')')
            if self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS,'-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL,'*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV_FLOAT,'/')
            if self.current_char == ':':
                self.advance()
                return self._colen()
            if self.current_char.isdigit():
                return self.get_number()
            if self.current_char == ',':
                self.advance()
                return Token(COMMA,',')
            
            self.error()
        return Token(EOF,None)

    def error(self):
        raise Exception("Invalid Character!")
    
    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()
    
    def _colen(self):
        if self.current_char == '=':
            self.advance()
            return Token(ASSGN,':=')
        return Token(COLON,':')
    
    def peek(self):
        pos =self.pos+1
        if pos > len(self.text) -1 :
            return None
        return self.text[pos]

    def _id(self):
        result = ''
        if self.current_char == '_': 
            result = '_'
            self.advance()
        while self.current_char is not None and self.current_char.isalnum():
            result+=self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result,Token(ID,result))
        return token
    
    def get_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char != '.':
            return Token(INT_CONST,int(result))
        self.advance()
        result+='.'
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(FLOAT_CONST,float(result))

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

#   PARSER
class Parser():
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
    
    def parse(self):
        tree  = self.program()
        if self.current_token.type != EOF:
            self.error()
        return tree
    
    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else: 
            self.error()

    def program(self):
        self.eat(PROGRAM)
        name_node  = self.variable()
        self.eat(SEMI)
        block = self.block()
        self.eat(DOT)
        return Program(name_node.value,block)
    
    def variable(self):
        token = self.current_token
        self.eat(ID)
        return Var(token)
    
    def block(self):
        declaration_nodes = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declaration_nodes,compound_statement)
    
    def declarations(self):
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.var_decl()
                declarations.extend(var_decl)
                self.eat(SEMI)
        return declarations
    
    def var_decl(self):
        nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type is not COLON:
            self.eat(COMMA)
            nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)
        type_space = self.type_spec()
        return [
            VarDecl(node,type_space) for node in nodes
        ]

    def type_spec(self):
        if self.current_token.type == INTEGER:
            node = Type(self.current_token)
            self.eat(INTEGER)
        if self.current_token.type == REAL:
            node = Type(self.current_token)
            self.eat(REAL)
        return node

    def compound_statement(self):
        node = Compound()
        self.eat(BEGIN)
        node.children = self.statement_list()
        self.eat(END)
        return node
    
    def statement_list(self):
        result = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            result.append(self.statement())
        return result
    
    def statement(self):
        if self.current_token.type == BEGIN:
            return self.compound_statement()
        elif self.current_token.type == ID:
            return self.assignment()
        else:
            return NoOp()
    
    def assignment(self):
        var_node = self.variable()
        token = self.current_token
        self.eat(ASSGN)
        expr = self.expr()
        return Assign(var_node,token,expr)
    
    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BnOp(node,token,self.term())
        return node 
    
    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV_INT,DIV_FLOAT):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV_INT:
                self.eat(DIV_INT)
            elif token.type == DIV_FLOAT:
                self.eat(DIV_FLOAT)
            node = BnOp(node,token,self.term())
        return node
    
    def factor(self):
        token = self.current_token
        if token.type == ID:
            self.eat(ID)
            return Var(token)
        elif token.type == INT_CONST:
            self.eat(INT_CONST)
            return Num(token)
        elif token.type == FLOAT_CONST:
            self.eat(FLOAT_CONST)
            return Num(token)
        elif token.type == PLUS:
            self.eat(PLUS)
            return UnOp(token,self.expr())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnOp(token,self.expr())
    
    def error(self):
        raise Exception("Invalid Syntax !")

class NodeVisitor():
    def visit(self,node):
        method_name = 'visit_'+type(node).__name__
        visitor = getattr(self,method_name, 'generic_visit')
        return visitor(node)

    def generic_visit(self,node):
        raise Exception("visit_{} does not exit".format(type(node).__name__))

class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self,parser):
        self.parser =parser
    
    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)
        print(self.GLOBAL_SCOPE)
    
    def visit_Program(self,program:Program):
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

    def visit_Compound(self, node:Compound):
        for child in node.children:
            self.visit(child)

#   MAIN 
if __name__ == '__main__':
    import sys
    text = open(sys.argv[1],'r+').read()
    lexer = Lexer(text)
    # while lexer.current_char is not None:
    #     print(lexer.next_token()) 
    parser = Parser(lexer)
    interpreter  = Interpreter(parser)
    interpreter.interpret()    
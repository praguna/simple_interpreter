from ast import Program,Var,Block,VarDecl,Type,NoOp,BnOp,Num,UnOp,Assign,Compound
from token import *

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
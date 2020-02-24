from ast import Program,Var,Block,VarDecl,Type,NoOp,BnOp,Num,UnOp,Assign,Compound,ProcedureDecl,Params
from token import *
from error import parser_error

#   PARSER
class Parser():
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
    
    def parse(self):
        # CALLER FUCTION FOR PARSING
        tree  = self.program()
        if self.current_token.type != Token_Type.EOF:
            self.error()
        return tree
    
    def eat(self,token_type):
        # MOVES TO THE NEXT TOKEN AFTER VALIDATION
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else: 
            self.error()

    def program(self):
        # PROGRAM : BLOCK DOT
        self.eat(Token_Type.PROGRAM)
        name_node  = self.variable()
        self.eat(Token_Type.SEMI)
        block = self.block()
        self.eat(Token_Type.DOT)
        return Program(name_node.value,block)
    
    def variable(self):
        # VAR : ID
        token = self.current_token
        self.eat(Token_Type.ID)
        return Var(token)
    
    def block(self):
        # BLOCK : DECLARATIONS COMPOUND_STATEMENT
        declaration_nodes = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declaration_nodes,compound_statement)
    
    def declarations(self):
        # DECLARATIONS :  VAR(VARDECL SEMI)+ (PROCEDURE ID (LPAREN FORMAL_PARAMETER_LIST RPAREN)? SEMI BLOCK SEMI)* 
        # | EMPTY 
        declarations = []
        if self.current_token.type == Token_Type.VAR:
            self.eat(Token_Type.VAR)
            while self.current_token.type == Token_Type.ID:
                var_decl = self.var_decl()
                declarations.extend(var_decl)
                self.eat(Token_Type.SEMI)
    
        while self.current_token.type == Token_Type.PROCEDURE:
            self.eat(Token_Type.PROCEDURE)
            name_node = self.variable()
            params = []
            if self.current_token.type == Token_Type.LPAREN:
                self.eat(Token_Type.LPAREN)
                params = self.formal_parameter_list()
                self.eat(Token_Type.RPAREN)
            self.eat(Token_Type.SEMI)
            block = self.block()
            self.eat(Token_Type.SEMI)
            declarations.append(ProcedureDecl(name_node.value, block,params))
            
        return declarations
    
    def formal_parameter_list(self):
        # FORMAL_PARAMETER_LIST : FORMAL_PARAMETERS | FORMAL_PARAMETERS SEMI FORMAL_PARAMETER_LIST
        parameter_list = self.formal_parameters()
        while self.current_token.type == Token_Type.SEMI:
            self.eat(Token_Type.SEMI)
            parameter_list.extend(self.formal_parameters())
        return parameter_list

    def formal_parameters(self):
        # FORMAL_PARAMETERS : ID (COMMA ID)* COLON TYPE_SPEC
        params = []
        vars = [self.current_token]
        self.eat(Token_Type.ID)
        while self.current_token.type == Token_Type.COMMA:
            self.eat(Token_Type.COMMA)
            vars.append(self.current_token)
            self.eat(Token_Type.ID)
        self.eat(Token_Type.COLON)
        type = self.type_spec()
        for var in vars:
            params.append(Params(Var(var),type))
        return params    
    
    def var_decl(self):
        # VARDECL : VAR(COMMA VAR)* : TYPESPEC
        nodes = [Var(self.current_token)]
        self.eat(Token_Type.ID)
        while self.current_token.type is not Token_Type.COLON:
            self.eat(Token_Type.COMMA)
            nodes.append(Var(self.current_token))
            self.eat(Token_Type.ID)
        self.eat(Token_Type.COLON)
        type_space = self.type_spec()
        return [
            VarDecl(node,type_space) for node in nodes
        ]

    def type_spec(self):
        # TYPESPEC : INTEGER | REAL
        if self.current_token.type == Token_Type.INTEGER:
            node = Type(self.current_token)
            self.eat(Token_Type.INTEGER)
        elif self.current_token.type == Token_Type.REAL:
            node = Type(self.current_token)
            self.eat(Token_Type.REAL)
        else:
            raise Exception('Error : unknown type {}'.format(self.current_token.value))
        return node

    def compound_statement(self):
        #COMPOUND_STATEMENT : BEGIN STATEMENT_LIST END
        node = Compound()
        self.eat(Token_Type.BEGIN)
        node.children = self.statement_list()
        self.eat(Token_Type.END)
        return node
    
    def statement_list(self):
        #STATEMENT_LIST : STATEMENT | STATEMENT SEMI STATEMENT_LIST
        result = [self.statement()]
        while self.current_token.type == Token_Type.SEMI:
            self.eat(Token_Type.SEMI)
            result.append(self.statement())
        return result
    
    def statement(self):
        # STATEMENT : EMPTY | ASSIGNMENT | COMPOUND_STATEMENT
        if self.current_token.type == Token_Type.BEGIN:
            return self.compound_statement()
        elif self.current_token.type == Token_Type.ID:
            return self.assignment()
        else:
            return NoOp()
    
    def assignment(self):
        #ASSIGNMENT : VAR ASSGN EXPR
        var_node = self.variable()
        token = self.current_token
        self.eat(Token_Type.ASSGN)
        expr = self.expr()
        return Assign(var_node,token,expr)
    
    def expr(self):
        # EXPR : TERM ((PLUS | MINUS)TERM)*
        node = self.term()
        while self.current_token.type in (Token_Type.PLUS,Token_Type.MINUS):
            token = self.current_token
            if token.type == Token_Type.PLUS:
                self.eat(Token_Type.PLUS)
            elif token.type == Token_Type.MINUS:
                self.eat(Token_Type.MINUS)
            node = BnOp(node,token,self.term())
        return node 
    
    def term(self):
        # FACTOR  : FACTOR ((MUL | DIV_INT | DIV_FLOAT) FACTOR)*
        node = self.factor()
        while self.current_token.type in (Token_Type.MUL, Token_Type.DIV, Token_Type.DIV_FLOAT):
            token = self.current_token
            if token.type == Token_Type.MUL:
                self.eat(Token_Type.MUL)
            elif token.type == Token_Type.DIV:
                self.eat(Token_Type.DIV)
            elif token.type == Token_Type.DIV_FLOAT:
                self.eat(Token_Type.DIV_FLOAT)
            node = BnOp(node,token,self.term())
        return node
    
    def factor(self):
        # FACTOR : ID | VAR | PLUS EXPR | MINUS EXPR | LPAREN EXPR RPAREN 
        token = self.current_token
        if token.type == Token_Type.ID:
            self.eat(Token_Type.ID)
            return Var(token)
        elif token.type == Token_Type.INT_CONST:
            self.eat(Token_Type.INT_CONST)
            return Num(token)
        elif token.type == Token_Type.FLOAT_CONST:
            self.eat(Token_Type.FLOAT_CONST)
            return Num(token)
        elif token.type == Token_Type.PLUS:
            self.eat(Token_Type.PLUS)
            return UnOp(token,self.expr())
        elif token.type == Token_Type.MINUS:
            self.eat(Token_Type.MINUS)
            return UnOp(token,self.expr())
    
    def error(self):
        raise parser_error(message="Parser Error")
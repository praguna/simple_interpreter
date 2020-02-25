from token import *
from error import lexer_error
# LEXER CLASS SCANS THE TEXT AND RETURNS TOKENS WHEN ONE IS ENCOUNTERED
class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.lineno = 1
        self.column = 1
        self.current_char = self.text[self.pos]
    
    def advance(self):
        if self.text[self.pos] == '\n':
            self.lineno+=1
            self.column = 0

        self.pos+=1
        if self.pos > len(self.text) -1:
            self.current_char = None
        else : 
            self.column+=1
            self.current_char = self.text[self.pos]

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
            if self.current_char == ':':
                self.advance()
                return self._colen()    
            if self.current_char.isdigit():
                return self.get_number()                    
            try:
                token_type = Token_Type(self.current_char)
            except ValueError:
                self.error()
            else:
                self.advance()
                return Token(token_type,value=self.current_char,lineno=self.lineno,column=self.column-1)
        return Token(type= Token_Type.EOF,value = None, lineno =self.lineno,column = self.column)

    def error(self):
        s = "Lexer Error on {lexeme} in line : {line}, column : {column}".format(
            lexeme = self.current_char,
            line = self.lineno,
            column = self.column
        )
        raise lexer_error(s)
    
    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()
    
    def _colen(self):
        lineno = self.lineno
        column  = self.column
        if self.current_char == '=':
            self.advance()
            return Token(Token_Type.ASSGN,':=',lineno=lineno,column=column)
        return Token(Token_Type.COLON,':',lineno=lineno,column=column)
    
    def peek(self):
        pos =self.pos+1
        if pos > len(self.text) -1 :
            return None
        return self.text[pos]

    def _id(self):
        lineno = self.lineno
        column  = self.column
        result = ''
        if self.current_char == '_': 
            result = '_'
            self.advance()
        while self.current_char is not None and self.current_char.isalnum():
            result+=self.current_char
            self.advance()
        token_type = RESERVED_KEYWORDS.get(result.upper(),Token_Type.ID)
        if token_type == Token_Type.ID:
            return Token(Token_Type.ID,result.upper(),lineno=lineno,column=column)
        return Token(token_type,token_type,lineno=lineno,column=column)
    
    def get_number(self):
        lineno = self.lineno
        column = self.column
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char != '.':
            return Token(Token_Type.INT_CONST,int(result),lineno=lineno,column=column)
        self.advance()
        result+='.'
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(Token_Type.FLOAT_CONST,float(result),lineno=lineno,column=column)
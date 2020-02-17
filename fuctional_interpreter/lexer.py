from token import *
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
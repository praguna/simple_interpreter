#TOKENS
INTEGER,PLUS,MINUS,MUL,DIV,EOF = ('INTEGER','PLUS','MINUS','MUL','DIV','EOF')
#TOKEN CLASS DEFINES THE TOKENS
class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return 'TOKEN({type},{value})'.format(type=self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

#LEXER CLASS FOR SCANNING TOKENS AND CHECKING SYNTACTIC VALIDITY
class Lexer():
    def __init__(self,text):
        self.text = text
        self.index = 0
        self.current_char = self.text[self.index]
    
    def error(self):
        raise Exception("Invalid Character")

    def advance(self):
        self.index+=1
        if self.index > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.index]

    def remove_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)

    def next_token(self):
        # returns tokens
        while self.current_char is not None:
            #Remove white spaces
            if self.current_char.isspace():
                self.remove_space()
                continue
            #Extract Integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())
            #Extract operators
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            #Otherwise throw an Error
            self.error()
        return Token(EOF, None)

class Interpreter():
    def __init__(self,lexer:Lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()
    
    def error(self):
        raise Exception("Invalid Syntax")

    def eat(self,type):
        if self.current_token.type == type:
            self.current_token = self.lexer.next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value
    
    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            if token.type == MUL:  
                self.eat(MUL)
                result *= self.factor()
            else: 
                self.eat(DIV)
                result /= self.factor()
        return result

    def expr(self):
        """
        Grammer:
            E : T((+|-)T)* -->expr
            T : F((*|/)F)* --> term
            F : (V) --> factor
        """
        #parser and interpreter section
        result = self.term()
        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            else:
                self.eat(MINUS)
                result -= self.term()
        return result
    

if __name__ == "__main__":
    while True:
        try:
            text = input("rewrite_calc_5>")
        except EOFError:
            break
        if not text: continue
        if text == "bye": break
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        print(interpreter.expr())
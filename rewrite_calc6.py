# Define All Tokens
INTEGER, PLUS, MINUS, MUL, DIV, LPARAN, RPARAN, EOF = (
    "INTEGER","PLUS","MINUS","MUL","DIV","LPARAN","RPARAN","EOF"
)

class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value
        
    def __str__(self):
        return "TOKEN({type},{value})".format(type = self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

class Lexer():
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
            if self.current_char == "*":
                self.advance()
                return Token(MUL,'*')
            if self.current_char == "+":
                self.advance()
                return Token(PLUS,'+')
            if self.current_char == "-":
                self.advance()
                return Token(MINUS,'-')
            if self.current_char == "/":
                self.advance()
                return Token(DIV,'/')
            if self.current_char == "(":
                self.advance()
                return Token(LPARAN,'(')
            if self.current_char == ")":
                self.advance()
                return Token(RPARAN,')')                                                                
            self.error()
        return Token(EOF,None)

class Interpreter():
    def __init__(self,lexer:Lexer):
        self.lexer =lexer
        self.current_token = self.lexer.next_token()

    def error(self):
        raise Exception("Syntax Error")

    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            self.error()
        
    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPARAN:
            self.eat(LPARAN)
            result = self.expr()
            self.eat(RPARAN)
            return result

    def expr(self):
        """
        E : T((PLUS|MINUS)T)*
        T : F((MUL|DIV)F)*
        F : INT | (E)
        """
        result = self.term()
        while self.current_token.type in (PLUS , MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result+=self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result-=self.term()

        return result
    
    def expr_interpreter(self):
        result = self.expr()
        if self.current_token.type is not EOF:
            self.error()
        return result        

if __name__ == "__main__":
    while True:
        try:
            text = input("rewrite_calc_6>")
        except EOFError: break
        if not text: continue
        if text == "bye": break
        interpreter = Interpreter(Lexer(text))
        print(interpreter.expr_interpreter())
        # lexer = Lexer(text)
        # for i in text:
        #     print(lexer.next_token())
from lexer import Lexer
from interpreter import Interpreter
from pascal_parser import Parser

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
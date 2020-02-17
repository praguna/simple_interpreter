from lexer import Lexer
from interpreter import Interpreter
from pascal_parser import Parser
from symbol_table import SymbolTableBuilder

#   MAIN 
if __name__ == '__main__':
    import sys
    text = open(sys.argv[1],'r+').read()
    lexer = Lexer(text)
    # while lexer.current_char is not None:
    #     print(lexer.next_token()) 
    parser = Parser(lexer)
    tree = parser.parse()
    symbuilder = SymbolTableBuilder()
    symbuilder.visit(tree)
    print("ALL CLEAR !")
    print(symbuilder.symtab)
    interpreter  = Interpreter(tree)
    interpreter.interpret()
    print("Global Memory State !")
    print(interpreter.GLOBAL_SCOPE)    
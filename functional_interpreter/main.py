from lexer import Lexer
from interpreter import Interpreter
from pascal_parser import Parser
from static_semantics import SemanticAnalyzer

global  SEMANTIC_LOGS 
#   MAIN 
if __name__ == '__main__':
    import sys
    SEMANTIC_LOGS = False
    text = open(sys.argv[1],'r+').read()
    lexer = Lexer(text)
    # while lexer.current_char is not None:
    #     print(lexer.next_token()) 
    try:
        if sys.argv.index("--scope"):
            SEMANTIC_LOGS = True
    except:pass
    parser = Parser(lexer)
    tree = parser.parse()
    symbuilder = SemanticAnalyzer(console=SEMANTIC_LOGS)
    symbuilder.visit(tree)
    print("ALL CLEAR !")
    # # print(symbuilder.current_scope)
    interpreter  = Interpreter(tree)
    interpreter.interpret()
    print("Global Memory State !")
    print(interpreter.GLOBAL_SCOPE)    
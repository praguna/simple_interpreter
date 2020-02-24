from enum import Enum
# TOKEN DEFINES BASIC UNIT OF TEXT RECOGNISED AT A TIME BY THE INTERPRETER
# TOKEN CLASS 
class Token():
    def __init__(self,type = None,value = None,lineno=None,column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column
    def __str__(self):
        return "TOKEN({type},{value} , position = {lineno} : {column})".format(type = self.type,
        value = self.value, lineno = self.lineno, column = self.column)

    def __repr__(self):
        return self.__str__()

# THESE KEYWORDS DEFINE THE BUILT IN TYPES
class Token_Type(Enum):
    #Single character tokens
    PLUS = "+"
    MINUS = "-"
    DIV_FLOAT = "/"
    SEMI = ";"
    COLON = ":"
    ASSGN = ":="
    LPAREN = "("
    MUL = "*"
    RPAREN = ")"
    DOT = "."
    COMMA = ","
    #Section of reserved keywords
    PROGRAM = "PROGRAM"
    BEGIN = "BEGIN"
    VAR = "VAR"
    DIV = "DIV"
    INTEGER = "INTEGER"
    REAL = "REAL"
    PROCEDURE = "PROCEDURE"
    END = "END"
    #end of reserved words section
    #misc
    EOF = "EOF"
    ID = "ID"
    INT_CONST = "INT_CONST"
    FLOAT_CONST = "FLOAT_CONST"
    

def build_reserved_keywords():
    # returns a dictionary of reserved words
    tokens = list(Token_Type)
    start_index = tokens.index(Token_Type.PROGRAM)
    end_index = tokens.index(Token_Type.END)
    result = {
        ttype.value : ttype
        for ttype in tokens[start_index:end_index+1]
    }
    return result

RESERVED_KEYWORDS = build_reserved_keywords()
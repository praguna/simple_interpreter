# TOKEN
PROGRAM,INTEGER,REAL,PLUS,MINUS,DIV_INT,DIV_FLOAT,SEMI,COLON,ASSGN,LPAREN,MUL,RPAREN,EOF,DOT,ID,BEGIN,END,VAR,INT_CONST,FLOAT_CONST,COMMA =(
    "PROGRAM","INTEGER","REAL","PLUS","MINUS","DIV_INT","DIV_FLOAT","SEMI","COLON","ASSGN","LPAREN","MUL",
    "RPAREN","EOF","DOT","ID","BEGIN","END","VAR","INT_CONST","FLOAT_CONST","COMMA"
)
# TOKEN CLASS
class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return "TOKEN({type},{value})".format(type = self.type,value = self.value)
    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    "BEGIN": Token(BEGIN,BEGIN),
    "END" : Token(END,END),
    "VAR" : Token(VAR, VAR),
    "PROGRAM" : Token(PROGRAM,PROGRAM),
    "DIV" : Token(DIV_INT,DIV_INT),
    "INTEGER" : Token(INTEGER,INTEGER),
    "REAL": Token(REAL,REAL)
}
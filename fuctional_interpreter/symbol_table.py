from visitor import NodeVisitor
class Symbol():
    def __init__(self,name,type= None):
        self.name = name
        self.type = type
    
class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name
    
    __repr__ = __str__

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type=type)
    
    def __str__(self):
        return '<{name}:{type}>'.format(name = self.name,type =self.type)
    
    __repr__ = __str__ 

class SymbolTable():
    def __init__(self):
        self._symbol = {}
    
    def define(self,symbol):
        print("Define %s"%symbol)
        self._symbol[symbol.name] = symbol
    
    def lookup(self,name):
        print("Lookup %s"%name)
        type = self._symbol.get(name)
        return type

    def __str__(self):
        s = 'Symbols : {}'.format(
            [symbol for symbol in self._symbol.values()]
        )
        return s

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
    
    def visit_Program(self,node):
        self.visit(node.block)

    def visit_Block(self,node):
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)
    
    def visit_UnOp(self,node):
        self.visit(node.expr)

    def visit_Compound(self,node):
        for child in node.children:
            self.visit(child)

    def visit_VarDecl(self,node):
        type_name = node.type_node.value
        name  = node.var_node.value
        type = BuiltInTypeSymbol(type_name)
        var = VarSymbol(name,type)
        self.symtab.define(var)

    def visit_Num(self,node):
        pass

    def visit_BnOp(self,node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_NoOp(self,node):
        pass
    
    def visit_Assign(self,node):
        var_name = node.left.value
        type = self.symtab.lookup(var_name)
        if type == None:
            raise NameError(repr(var_name))

    def visit_Num(self,node):
        pass

    def visit_Var(self,node):
        var_name = node.value
        type = self.symtab.get(var_name)
        if type == None: 
            raise NameError(repr(var_name))


# int_type = BuiltInTypeSymbol("INTEGER")
# x = VarSymbol("a",int_type)
# print(x)
# z = BuiltInTypeSymbol("FLOAT")
# y = VarSymbol("b",z)
# symbol_table = SymbolTable()
# symbol_table.define(int_type)
# symbol_table.define(y)
# symbol_table.define(z)
# symbol_table.define(x)
# print(symbol_table.lookup(x.name))
# print(symbol_table)


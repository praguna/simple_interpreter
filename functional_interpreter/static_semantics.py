from visitor import NodeVisitor
from symbol_type import *
from error import semantic_error,ErrorCode

class ScopedSymbolTable():
    def __init__(self,scope_level,scope_name,enclosing_scope = None,LOGS = False):
        self._symbol = {}
        self.scope_level = scope_level
        self.scope_name = scope_name
        self.enclosing_scope = enclosing_scope
        self.LOGS = LOGS
        
    def builtin(self):
        self.define(BuiltInTypeSymbol("INTEGER"))
        self.define(BuiltInTypeSymbol("REAL"))

    def define(self,symbol):
        self.logs("Define %s"%symbol)
        self._symbol[symbol.name] = symbol
    
    def lookup(self,name,current_scope_only = False):
        self.logs("Lookup {name} (Scope {scope_name})".format(name = name,scope_name = self.scope_name))
        symbol = self._symbol.get(name)
        if symbol is not None:
            return symbol
        if current_scope_only:
            return None
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        return symbol

    def __str__(self):
        s = 'Scoped Symbol Table \n' + "--"*10+'\n\
            level : {level}   Scope-Name : {name} \n'.format(level = self.scope_level ,name =self.scope_name)\
            + "--"*10 + '\n'
        for symbol in self._symbol.values():
            s+=symbol.name +" : " + str(symbol) + "\n"
        return s
    
    __repr__ = __str__

    def logs(self,message):
        if self.LOGS: print(message)

class SemanticAnalyzer(NodeVisitor):
    def __init__(self,console = False):
        self.current_scope = None
        self.console  = console
        self.__init__builtins()
    
    def __init__builtins(self):
        self.current_scope = ScopedSymbolTable(0,"BuiltIn",LOGS=self.console)
        self.current_scope.builtin()
        self.logs(self.current_scope)

    def visit_Program(self,node):
        self.logs("Entering Global Scope :")
        global_scope = ScopedSymbolTable(scope_level=self.current_scope.scope_level+1,\
            scope_name="global",enclosing_scope=self.current_scope,LOGS=self.console)
        self.current_scope = global_scope
        self.visit(node.block)
        self.logs(global_scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.logs("Leaving Global Scope :")

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
        type = self.current_scope.lookup(type_name)
        if self.current_scope.lookup(name,current_scope_only = True) is not None:
            raise semantic_error("{errorcode} : {name} is already declared".format(errorcode = ErrorCode.DUPLICATE_ID.value,name = node.var_node.token))
        var = VarSymbol(name,type)
        self.current_scope.define(var)

    def visit_Num(self,node):
        pass

    def visit_BnOp(self,node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_NoOp(self,node):
        pass
    
    def visit_Assign(self,node):
        var_name = node.left.value
        type = self.current_scope.lookup(var_name)
        if type == None:
            raise semantic_error('{errorcode} : {var}'.format(errorcode = ErrorCode.ID_NOT_FOUND.value, var = node.left.token))

    def visit_Num(self,node):
        pass

    def visit_Var(self,node):
        var_name = node.value
        var_symbol = self.current_scope.get(var_name)
        if var_symbol == None: 
            raise Exception('ERROR : {var} not found'.format(var = node.token))
    
    def visit_ProcedureDecl(self,node):
        proc_name = node.name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.define(proc_symbol)
        self.logs("Enter Procedure Scope : %s"%proc_name)
        procedure_scope = ScopedSymbolTable(
            scope_level=self.current_scope.scope_level+1,scope_name=proc_name,enclosing_scope=self.current_scope,LOGS=self.console
        )
        self.current_scope = procedure_scope
        for param in node.params:
            name = param.var_node.value
            type = self.current_scope.lookup(param.type_node.value)
            var_symbol = VarSymbol(name,type)
            self.current_scope.define(var_symbol)
            proc_symbol.params.append(var_symbol)
        self.visit(node.block)
        self.logs(self.current_scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.logs('Leaving Procedure Scope : %s'%proc_name)

    def visit_Params(self, node):
        pass

    def logs(self,message):
        if self.console: print(message)
        

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
class Symbol():
    def __init__(self,name,type= None):
        self.name = name
        self.type = type
    
class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return '<{class_name}({name})>'.format(class_name = self.__class__.__name__,name = self.name)

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type=type)
    
    def __str__(self):
        return '<{class_name}({name}:{type})>'.format(class_name = self.__class__.__name__,\
            name = self.name,type =self.type)
    
    __repr__ = __str__ 

class ProcedureSymbol(Symbol):
    def __init__(self, name,params = None):
        super(ProcedureSymbol,self).__init__(name = name)
        self.params = params if params is not None else []
    
    def __str__(self):
        return '<{class_name}({name} , Parameters = {params})>'.format(class_name = self.__class__.__name__,\
             name = self.name, params =self.params)
    __repr__ = __str__
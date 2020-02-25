from enum import Enum
class ErrorCode(Enum):
    UNEXPECTED_TOKEN = "Unexpected Token Found"
    ID_NOT_FOUND = "Id not found"
    DUPLICATE_ID = "Duplicate Id Exists"
    pass


class Error(Exception):
    def __init__(self, error_code=None, token=None ,message = None):
        self.error_code  = error_code
        self.message = message
        self.token = token
        self.message = f'{self.__class__.__name__}:{message}'    

class lexer_error(Exception):
        pass

class parser_error(Exception):
        pass

class semantic_error(Exception):
        pass
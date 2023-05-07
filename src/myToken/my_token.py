class Token:
    def __init__(self,token_id = None,token_lexeme = None,token_line = None,attr = None) -> None:
        self.id = token_id
        self.lexeme = token_lexeme
        self.line = token_line
        self.attr = attr
        pass
    
    def set_attr(self,attr):
        self.attr = attr

    def __repr__(self) -> str:
        return f'[ Token ID : {self.id} '\
               f'Token Lexeme : {self.lexeme} '\
               f'Token Line : {self.line} ]'
        
        pass

def func():
    pass

if __name__ == '__main__':
    t = Token()

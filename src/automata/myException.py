class DuplicateStateException(Exception):
    '''
    Duplicate State
    '''
    def __init__(self,state):
        self.state = state
    def __str__(self):
        return repr(f'duplicate state \"{self.state}\"') 

class NoneexistentStateException(Exception):
    '''
    Nonexistent State
    '''
    def __init__(self,state):
        self.state = state
    def __str__(self):
        return repr(f'noneexistent state \"{self.state}\"') 

class NoneexistentLetterException(Exception):
    '''
    Nonexistent Letter
    '''
    def __init__(self,letter):
        self.letter = letter
    def __str__(self):
        return repr(f'noneexistent letter \"{self.letter}\"') 

class IncorrectLetterlLengthException(Exception):
    '''
    incorrect letterl length
    '''
    def __init__(self,letter):
        self.letter = letter
    def __str__(self):
        return repr(f'wrong letter \"{self.letter}\", the letter length must be 1 ') 

class NonexistentTransitionRule(Exception):
    '''
    nonexistent transition rule
    '''
    def __init__(self,state,ch):
        self.state = state
        self.ch = ch
    def __str__(self):
        return repr(f'nonexistent transition rule on state {self.state} for letter {self.ch}')
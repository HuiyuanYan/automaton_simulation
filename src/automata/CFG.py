import sys
import os
import copy
from typing import List,Set,Callable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from container.multi_key_dict import multi_key_dict
from automata.myException import LL_1_ConflictingEntry
class CFG_Production:
    def __init__(self,head = None,body = None,action:Callable = None) -> None:
        self._head = head
        self._body = []
        self._action = action # for parser use
        self._is_epsilon = False
        if body != None:
            self.set_production_body(body)
            
    def set_production_head(self,head:str)->None:
        self._head = head

    def set_production_body(self,body:List[str])->None:
        if len(body) == 1 and body[0] == 'ε':
            self._is_epsilon = True
        for elem in body:
            self._body.append(elem)

    def set_production_action(self,action:Callable = None):
        self._action = action


    def body(self):
        return self._body.copy()
    
    def head(self):
        return self._head

    def is_epsilon(self):
        return self._is_epsilon

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self) -> str:
        if self._head == None:
            return ''
        s = f'{self._head} -> '
        for elem in self._body:    
            s += elem
        return s

class LL1_analysis_table():
    def __init__(self) -> None:
        self.__table = multi_key_dict(2)
    
    def add_entry(self,variable:str,terminal:str,production:CFG_Production):
        try:
            if (variable,terminal) not in self.__table.keys():
                self.__table.set_value((variable,terminal),production)
            else:
                raise LL_1_ConflictingEntry(variable,
                                            terminal,
                                            self.__table.get_value((variable,terminal))[0].__str__(),
                                            production.__str__())
        except LL_1_ConflictingEntry as e:
            sys.stderr.write(e.__str__()+'\n')
            assert 0
        return
    
    def get_entry(self,variable,terminal):
        return self.__table.get_value((variable,terminal))
    
    def __contains__(self,keys:tuple):
        return keys in self.__table

    def __str__(self) -> str:
        s = ''
        for key,val in self.__table.items():
            s += f'{key} : {val}\n'
        return s



class CFG:
    def __init__(self) -> None:
        self.__variables = {}
        self.__terminals = {}
        self.__productions = dict()
        self.__epsilon = 'ε'
        self.__end_symbol = '$'
        self.__start_variable = None
        self.__LL_1_analysis_table = None
    
    def set_variables(self,variables:Set[str]):
        self.__variables = variables.copy()
    
    def set_terminals(self,terminals:Set[str]):
        self.__terminals = terminals.copy()

    def set_start_variable(self,start_variable:str):
        assert start_variable in self.__variables
        self.__start_variable = start_variable

    def add_production(self,head:str,body:List[str],action:Callable = None):
        assert head in self.__variables
        for elem in body:
            assert elem in self.__variables or self.__terminals or elem == self.__epsilon
        if head not in self.__productions:
            self.__productions[head] = []
        production = CFG_Production(head,body,action)
        self.__productions[head].append(production)       
    def epsilon(self):
        return self.__epsilon
    
    def variables(self):
        return self.__variables.copy()
    
    def terminals(self):
        return self.__terminals.copy()
    
    def productions(self):
        return self.__productions.copy()

    def start_variable(self):
        return self.__start_variable
    
    def end_symbol(self):
        return self.__end_symbol

    
    
    
    

    def __str__(self) -> str:
        s = f'Variables      : {self.__variables}\n'\
            f'Terminals      : {self.__terminals}\n'\
            f'Start_Variable : {self.__start_variable}\n'\
            f'Productions    : \n'
        for val in self.__productions.values():
            for production in val:
                s += f'{production}\n'
        return s

class LL_1_parser:
    def __init__(self,input_CFG = None) -> None:
        self.__LL_1_analysis_table = None
        self.__CFG = input_CFG
        pass
    def construct_LL_1_analysis_table(self):
        first = dict()
        follow = dict()

        terminals = self.__CFG.terminals()
        variables = self.__CFG.variables()
        productions = self.__CFG.productions()
        epsilon = self.__CFG.epsilon()
        start_variable = self.__CFG.start_variable()
        end_symbol = self.__CFG.end_symbol()

        def union_set(s1:set,s2:set):
            if len(s2 - s1) != 0:
                s1 |= s2
                return True
            else:
                return False

        def get_FIRST():
            nonlocal first
            def update_FIRST(symbol:str)->bool:
                ret = False
                if symbol in terminals:
                    ret |= union_set(first[symbol],{symbol})

                elif symbol in variables:
                    for production in productions[symbol]:
                        if production.is_epsilon():
                            ret |= union_set(first[symbol],{epsilon})

                        else:
                            all_epsilon = True
                            for elem in production._body:
                                if all_epsilon == False:
                                    break
                                if elem in terminals:
                                    ret |= union_set(first[symbol],{elem})
                                    all_epsilon = False

                                elif elem in variables:
                                    ret |= union_set(first[symbol],first[elem]-{epsilon})
                                    if epsilon not in first[elem]:
                                        all_epsilon = False
                            if all_epsilon == True:
                                ret |= union_set(first[symbol],{epsilon})
                return ret
            # Initialize
            for terminal in terminals:
                first[terminal] = set()
            for var in variables:
                first[var] = set()
            
            updated = False
            while True:
                updated = False
                for terminal in terminals:
                    updated |= update_FIRST(terminal)
                for var in variables:
                    updated |= update_FIRST(var)
                if updated == False:
                    break
            return
            
        def get_FOLLOW():
            nonlocal first,follow
            # Initialize
            def update_FOLLOW():
                ret = False
                for head,production_list in productions.items():
                    for production in production_list:
                        if production.is_epsilon() == False:
                            body = production.body()
                            body_len = len(body)
                            for i in range(0,body_len):
                                if i < body_len - 1:
                                    ret |= union_set(follow[body[i]],first[body[i+1]]-{epsilon})
                            all_epsilon = True
                            for i in range(body_len -1,-1,-1):
                                if all_epsilon == False:
                                    break
                                ret |= union_set(follow[body[i]],follow[head])
                    
                                if epsilon not in first[body[i]]:
                                    all_epsilon = False
                return ret
                
            follow = dict()
            for terminal in terminals:
                follow[terminal] = set()
            for var in variables:
                follow[var] = set()

            follow[start_variable].add('$')
            updated = False
            while True:
                updated = update_FOLLOW()
                if updated == False:
                    break
            return
        

        def get_body_first(body:List[str])->set:
            nonlocal first
            s = set()
            all_epsilon = True
            for elem in body:
                if all_epsilon == False:
                    break
                if elem == epsilon:
                    s.add(epsilon)
                    break
                s |= (first[elem]-{epsilon})
                if epsilon not in first[elem]:
                    all_epsilon = False
            if all_epsilon == True:
                s.add(epsilon)
            return s

        get_FIRST()
        get_FOLLOW()

        self.__LL_1_analysis_table = LL1_analysis_table()
        for head,production_list in productions.items():
            for production in production_list:
                body = production.body()
                body_first = get_body_first(body)
                # For a in 'body_first', add production to M[A,a] if a in 'terminals'.
                for symbol in body_first:
                    if symbol in terminals:
                        self.__LL_1_analysis_table.add_entry(head,symbol,production)
                if epsilon in body_first:
                    for symbol in follow[head]:
                        if symbol in terminals or symbol == end_symbol:
                            self.__LL_1_analysis_table.add_entry(head,symbol,production)
        print(first)
        print(follow)
        print(self.__LL_1_analysis_table)

    def parse(self,input:str,verbose = False):
        assert self.__LL_1_analysis_table != None
        assert self.__CFG != None
        def print_identifier():
            nonlocal input_suffix,input_ptr,symbol_stack,length,action
            print(f'Matched_Str   : {input_suffix[0:input_ptr]}\n'\
                  f'Symbol_Stack  : {symbol_stack}\n'\
                  f'Unmatched_Str : {input_suffix[input_ptr:length]}\n'\
                  f'Action        : {action}\n')
        
        end_symbol = self.__CFG.end_symbol()
        start_variable = self.__CFG.start_variable()
        terminals = self.__CFG.terminals()

        input_suffix = input + end_symbol
        length = len(input_suffix)
        symbol_stack = [end_symbol,start_variable]

        action = ''
        # initialize
        input_ptr = 0
        top = symbol_stack[len(symbol_stack)-1]
        if verbose == True:
            print_identifier()
        # analysis
        while top != end_symbol:
            ch = input_suffix[input_ptr]
            if top == ch:
                symbol_stack.pop()
                input_ptr += 1
                action = f'match \'{top}\''
            elif top in terminals:
                action = f'error'
            elif (top,ch) not in self.__LL_1_analysis_table:
                action = f'error'
            elif (top,ch) in self.__LL_1_analysis_table:
                production = self.__LL_1_analysis_table.get_entry(top,ch)
                action = f'output {production}'
                symbol_stack.pop()
                if production.is_epsilon() == False:
                    # reversed
                    for elem in production.body()[::-1]:
                        symbol_stack.append(elem)
                # do production action
                if production._action is not None:
                    production._action()

            if verbose == True:
                print_identifier()
            if action == 'error':
                return False
            top = symbol_stack[len(symbol_stack)-1]
        if verbose == True:
            print(f'Accept input : \'{input}\'\n')
        return True

class LALR_1_parser:
    def __init__(self) -> None:
        pass

if __name__ == '__main__':
    pass
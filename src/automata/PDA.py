import sys
import os
from typing import List,Dict,Tuple
from graphviz import Digraph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automata.config import default_save_path
from container.multi_key_dict import multi_key_dict
class PDA_Template:
    def __init__(self) -> None:
        self.__input_symbols = set()
        self.__pushdown_symbols = set()
        self.__states = set()
        self.__transitions = multi_key_dict(3)
        self.__initial_state = ''
        self.__initial_symbol = ''
        self.__epsilon = 'ε'
    def set_input_symbols(self,input_symbols:set[str]):
        self.__input_symbols = input_symbols.copy()        
        
    def set_pushdown_symbols(self,pushdown_symbols:set[str]):
        self.__pushdown_symbols = pushdown_symbols.copy()
        
    def add_states(self,states:List[str]):
        self.__states = set(states)
        
    def add_state(self,state:str):
        self.__states.add(state)
               
    def add_transition(self,src_state:str,input_symbol:str,pre_symbol:str,target_state:str,next_symbols:str):
        assert src_state in self.__states
        assert target_state in self.__states
        assert pre_symbol in self.__pushdown_symbols
        assert input_symbol in self.__input_symbols or input_symbol == self.__epsilon
        if len(next_symbols) <= 1:
            assert next_symbols in self.__pushdown_symbols or next_symbols == self.__epsilon
        else:
            for symbol in next_symbols:
                assert symbol in self.__pushdown_symbols
        param = (src_state,input_symbol,pre_symbol)
        if param not in self.__transitions:
            self.__transitions.set_value(param,set())
        self.__transitions.get_value(param).add((target_state,next_symbols))

    def add_transitions(self,transitions:Dict[str,List[Tuple[str,str,str,str]]]):
        for src,val in transitions.items():
            for pre_symbol,input_symbol,target,next_symbols in val:
                self.add_transition(src,pre_symbol,input_symbol,target,next_symbols)
    
    def set_initial_symbol(self,initial_symbol:str):
        assert initial_symbol in self.__pushdown_symbols
        self.__initial_symbol = initial_symbol
    
    def set_initial_state(self,initial_state:str):
        assert initial_state in self.__states
        self.__initial_state = initial_state

    def __get_str(self) -> str:
        return  f"Input_symbols    : {self.__input_symbols}\n"\
                f"Epsilon          : {self.__epsilon}\n"\
                f"Pushdown_symbols : {self.__pushdown_symbols}\n"\
                f"States           : {self.__states}\n"\
                f"Initial_state    : {self.__initial_state}\n"\
                f"Initial_symbol   : {self.__initial_symbol}\n"\
                f"Transitions      : \n{self.__transitions}"
    
    def input_symbols(self):
        return self.__input_symbols.copy()
    
    def epsilon(self):
        return self.__epsilon
    
    def pushdown_symbols(self):
        return self.__pushdown_symbols.copy()
    
    def states(self):
        return self.__states.copy()
    
    def initial_state(self):
        return self.__initial_state
    
    def initial_symbol(self):
        return self.__initial_symbol
    
    def transitions(self):
        return self.__transitions.copy()
    

class PDA_F(PDA_Template):
    """PDA accepted by final states.
    """
    def __init__(self) -> None:
        super().__init__()
        self.__finish_states = set()
           
    def set_finish_states(self,finish_states:set[str]):
        self.__finish_states = finish_states.copy()
        
    def draw(self,name = 'PDA',path:str = default_save_path):
        G = Digraph(filename=(path+name))
        for state in self._PDA_Template__states:
            if state in self.__finish_states:
                G.node(state,state,shape = 'doublecircle')
            else:
                G.node(state,state,shape = 'circle')
            if state == self._PDA_Template__initial_state:
                G.node('start','start',shape = 'none')
                G.edge('start',state)
        edges_list = []
        items = self._PDA_Template__transitions.items()
        for key,val in items:
            src = key[0]
            input_symbol = key[1]
            pre_symbol = key[2]

            for target,next_symbols in val:
                ifFind = False
                for i in range(0,len(edges_list)):
                    if src == edges_list[i][0] and target == edges_list[i][1]:
                        ifFind = True
                        edges_list[i][2] += (f'\n{input_symbol},{pre_symbol}/{next_symbols}')
                        break
                if ifFind == False:
                    edges_list.append([src,target,f'{input_symbol},{pre_symbol}/{next_symbols}'])          
                
        
        # Add edges in the list to the directed graph
        for src,target,label in edges_list:
            G.edge(src,target,label)
        G.attr(rankdir = 'LR')
        G.view()
        return

    def run(self,input_str:str,verbose = False)->bool:
        """Test membership of input_str, accepted by final states.
        """
        transitions = self._PDA_Template__transitions
        epsilon = self._PDA_Template__epsilon
        def recursive_simulate(state:str,input_symbol_idx:str,stack_symbol:str,st:List[str]):
            nonlocal transitions,epsilon
            if state in self.__finish_states:
                return True
            if input_symbol_idx >= len(input_str):
                identifier_list = [(state,epsilon,stack_symbol)]
            else:
                identifier_list = [(state,input_str[input_symbol_idx],stack_symbol),(state,epsilon,stack_symbol)]
            
            for identifier in identifier_list:
                if identifier not in transitions:
                    continue
                for target,next_symbols in transitions.get_value(identifier):
                    tmp_st = st.copy()
                    if len(tmp_st) != 0:
                        tmp_st.pop()
                    if next_symbols != epsilon:
                        for symbol in next_symbols:
                            tmp_st.append(symbol)
                    if len(tmp_st) != 0:
                        tmp_stack_symbol = tmp_st[len(tmp_st)-1]
                    else:
                        tmp_stack_symbol = epsilon
                    result = recursive_simulate(target,input_symbol_idx+1,tmp_stack_symbol,tmp_st)
                    if result == True:
                        return True
            return False
        initial_symbol = self._PDA_Template__initial_symbol
        initial_state = self._PDA_Template__initial_state
        assert len(initial_symbol) == 1  
        stack = [initial_symbol]
        return recursive_simulate(initial_state,0,initial_symbol,stack)

    def finish_states(self):
        return self.__finish_states.copy()

    def __str__(self) -> str:
        return self._PDA_Template__get_str() + f"Finish_states    : {self.__finish_states}\n"

class PDA_E(PDA_Template):
    """PDA accepted by final states.
    """
    def __init__(self) -> None:
        super().__init__()
        
    def draw(self,name = 'PDA',path:str = default_save_path):
        G = Digraph(filename=(path+name))
        for state in self._PDA_Template__states:
            G.node(state,state,shape = 'circle')
            if state == self._PDA_Template__initial_state:
                G.node('start','start',shape = 'none')
                G.edge('start',state)
        edges_list = []
        items = self._PDA_Template__transitions.items()
        for key,val in items:
            src = key[0]
            input_symbol = key[1]
            pre_symbol = key[2]

            for target,next_symbols in val:
                ifFind = False
                for i in range(0,len(edges_list)):
                    if src == edges_list[i][0] and target == edges_list[i][1]:
                        ifFind = True
                        edges_list[i][2] += (f'\n{input_symbol},{pre_symbol}/{next_symbols}')
                        break
                if ifFind == False:
                    edges_list.append([src,target,f'{input_symbol},{pre_symbol}/{next_symbols}'])          
                
        
        # Add edges in the list to the directed graph
        for src,target,label in edges_list:
            G.edge(src,target,label)
        G.attr(rankdir = 'LR')
        G.view()
        return

    def run(self,input_str:str,verbose = False)->bool:
        """Test membership of input_str, accepted by final states.
        """
        transitions = self._PDA_Template__transitions
        epsilon = self._PDA_Template__epsilon
        def recursive_simulate(state:str,input_symbol_idx:str,stack_symbol:str,st:List[str]):
            nonlocal transitions,epsilon
            if len(st) == 0:
                return True
            if input_symbol_idx >= len(input_str):
                identifier_list = [(state,epsilon,stack_symbol)]
            else:
                identifier_list = [(state,input_str[input_symbol_idx],stack_symbol),(state,epsilon,stack_symbol)]
            
            for identifier in identifier_list:
                if identifier not in transitions:
                    continue
                for target,next_symbols in transitions.get_value(identifier):
                    tmp_st = st.copy()
                    if len(tmp_st) != 0:
                        tmp_st.pop()
                    if next_symbols != epsilon:
                        for symbol in next_symbols:
                            tmp_st.append(symbol)
                    if len(tmp_st) != 0:
                        tmp_stack_symbol = tmp_st[len(tmp_st)-1]
                    else:
                        tmp_stack_symbol = epsilon
                    result = recursive_simulate(target,input_symbol_idx+1,tmp_stack_symbol,tmp_st)
                    if result == True:
                        return True
            return False
        initial_symbol = self._PDA_Template__initial_symbol
        initial_state = self._PDA_Template__initial_state
        assert len(initial_symbol) == 1  
        stack = [initial_symbol]
        return recursive_simulate(initial_state,0,initial_symbol,stack)

    def __str__(self) -> str:
        return self._PDA_Template__get_str()

if __name__ == '__main__':

    pass

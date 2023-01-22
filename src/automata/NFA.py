import os
import sys
import copy
from typing import List,Dict,Tuple
from graphviz import Digraph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automata.config import default_save_path
from automata.myException import DuplicateStateException,NoneexistentStateException,NoneexistentLetterException,\
    IncorrectLetterlLengthException,NonexistentTransitionRule

class NFA:
    """NonDeterministic Finite Automata
    """
    def __init__(self):
        self.__Q = [] # states
        self.__alphabet = []
        self.__deltas = {}
        self.__q0 = '' # start state
        self.__finish_states = [] # finish state
        self.__epsilon = 'ε'
        pass

    def add_state(self,state:str):
        '''
        Add a transition state to NFA.
        '''
        try:
            if state in self.__Q:
                raise DuplicateStateException(state)
            else:
                self.__Q.append(state)
        except DuplicateStateException as e:
            sys.stderr.write(e.__str__()+'\n')
            return

    def add_states(self,states:List[str]):
        '''
        Add states to NFA.
        '''
        for state in states:
            self.add_state(state)
    
    def set_q0(self,q0:str):
        '''
        Set start states for NFA.
        '''
        try:
            if q0 in self.__Q:
                self.__q0 = q0
            else:
                raise NoneexistentStateException(q0)
        except NoneexistentStateException as e:
            self.__q0 = ''
            sys.stderr.write(e.__str__()+'\n')
            return
    
    def set_finish_states(self,finish_states:List[str]):
        '''
        Set finish states for NFA.
        '''
        for f in finish_states:
            try:
                if f in self.__Q:
                    if f not in self.__finish_states:
                        self.__finish_states.append(f)
                else:
                    raise NoneexistentStateException(f)
            except NoneexistentStateException as e:
                self.__finish_states.clear()
                sys.stderr.write(e.__str__()+'\n')
                return
    
    def set_alphabet(self,alphabet:List[str]):
        '''
        Set alphabet for NFA.
        '''
        for letter in alphabet:
            try:
                assert letter != self.__epsilon # letter: != Epsilon
                if len(letter) != 1:
                    raise IncorrectLetterlLengthException(letter)
                else:
                    if letter not in self.__alphabet:
                        self.__alphabet.append(letter)
            except IncorrectLetterlLengthException as e:
                self.__alphabet.clear()
                sys.stderr.write(e.__str__()+'\n')
                return

    def add_delta(self,src:str,letter:str,targets:set[str]):
        '''
        Set transition for NFA.
        '''
        try:
            if src not in self.__Q:
                raise NoneexistentStateException(src)
            if letter != self.__epsilon and letter not in self.__alphabet:
                raise NoneexistentLetterException(letter)
            # Check whether each state in target is legal
            for target in targets:
                if target not in self.__Q:
                    raise NoneexistentStateException(target)
            
            if src not in self.__deltas:
                self.__deltas[src] = []
            # In NFA, delta allow different transfers on one character.
            
            # Find whether the transfer function on letter already exists.
            for first,second in self.__deltas[src]:
                if first == letter:
                    # Add new target state set if it exists.
                    second = second | targets
                    return
            
            # If there is no transfer function on letter, set it.
            self.__deltas[src].append((letter,targets))
        except NoneexistentStateException as e:
            sys.stderr.write(e.__str__()+'\n')
        except NoneexistentLetterException as e:
            sys.stderr.write(e.__str__()+'\n')
        return

    def set_deltas(self,deltas:Dict[str,List[Tuple[str,set[str]]]]):
        '''
        Set transitions for NFA.
        deltas: Set of transitions.
        transtion format: (src,(letter,targets))
        '''
        for key,value in deltas.items():
            for (letter,next) in value:
                self.add_delta(key,letter,next)
        return

    def epsilon(self):
        return copy.deepcopy(self.__epsilon)

    def Q(self):
        return copy.deepcopy(self.__Q)

    def q0(self):
        return copy.deepcopy(self.__q0)

    def alphabet(self):
        return copy.deepcopy(self.__alphabet)
    
    def finish_states(self):
        return copy.deepcopy(self.__finish_states)
    
    def deltas(self):
        return copy.deepcopy(self.__deltas)

    def run(self,input:str,verbose = False)->bool:
        """Simulate input string on NFA.

        Args:
            input (str): input string
            verbose (bool, optional): Output simulation process. Defaults to False.
        Return:
            Simulation result: True/False
        """
        try:
            for c in input:
                if c not in self.__alphabet:
                    raise NoneexistentLetterException(c)
        except NoneexistentLetterException as e:
            sys.stderr.write(e.__str__()+'\n')
            return False
        
        current_state_set = self.__epsilon_closure({self.q0()})
        for i in range(0,len(input)):
            if verbose == True:
                print(f'Pre    : {current_state_set}')
                print(f'Input  : {input}')
                print(f'Read   : '+i*' '+'^')
            current_state_set = self.__move(current_state_set,input[i])
            if current_state_set is None:
                return False
            current_state_set = self.__epsilon_closure(current_state_set)
            if verbose == True:
                print(f'Next   : {current_state_set}\n')

        for state in current_state_set:
            if state in self.__finish_states:
                return True
        return False

    def __move(self,states:set[str],c:str):
        """Change states according to current states 'states' and letter 'c'

        Args:
            states (set[str]): pre_states
            ch (str): letter
        """
        try:
            for s in states:
                if s not in self.__Q:
                    raise NoneexistentStateException(s)
            if c not in self.__alphabet:
                raise NoneexistentLetterException(c)
        except NoneexistentStateException as e:
            sys.stderr.write(e.__str__()+'\n')
            return None
        except NoneexistentLetterException as e:
            sys.stderr.write(e.__str__()+'\n')
            return None
        
        result = set()
        try:
            # NFA shuts down when and only when there is no transition in all states.
            shut_down = True
            for s in states:
                if s not in self.__deltas:
                    continue
                for (letter,next_states) in self.__deltas[s]:
                    if c == letter:
                        result = result | next_states
                        shut_down |= False
            if shut_down == False:
                raise NonexistentTransitionRule
            return result
        except NonexistentTransitionRule as e:
            sys.stderr.write(e.__str__()+'\n')
            return None
                    
        pass

    def __epsilon_closure(self,states:set[str])->set:
        """Find the Epsilon closure of the states set.

        Args:
            states (set[str]): states set

        Returns:
            set: epsilon closure of the states set
        """
        result = states.copy()
        for s in states:
            if s not in self.__deltas:
                continue
            else:
                for (letter,next_states) in self.__deltas[s]:
                    if letter == self.__epsilon:
                        result = result | next_states
        return result
    def draw(self,name = 'NFA',path:str = default_save_path,):
        """Draw picture for NFA.

        Args:
            name (str, optional): dest file name. Defaults to 'NFA'.
            path (str, optional): dest file dir. Defaults to default_save_path.
        """
        G = Digraph(filename=(path+name))
        for q in self.__Q:
            if q in self.__finish_states:
                G.node(q,q,shape = 'doublecircle')
            else:
                G.node(q,q,shape = 'circle')
            if q == self.__q0:
                G.node('start','start',shape = 'none')
                G.edge('start',self.__q0)
        
        # Temporary container for storing edge information.
        # format of element: [src,target,label]
        edges_list = []
        for key,val in self.__deltas.items():
            for(letter,next_satets) in val:
                for next in next_satets:
                    # Check whether the edge to be added has been recorded.
                    ifFind = False
                    for i in range(0,len(edges_list)):
                        if edges_list[i][0] == key and edges_list[i][1] == next:
                            # Add the description to the label
                            edges_list[i][2] += f',{letter}'
                            ifFind = True
                            break
                    if ifFind == False:
                        # Edge does not exist, add it to the list.
                        edges_list.append([key,next,letter])
        
        # Add edges in the list to the directed graph
        for src,target,label in edges_list:
            G.edge(src,target,label)
        G.attr(rankdir = 'LR')
        G.view()
        return

if __name__ == "__main__":
    n = NFA()
    n.set_alphabet(['0','1'])
    n.add_states(['q0','q1','q2'])
    n.set_q0('q0')
    n.set_finish_states(['q2'])
    n.set_deltas(
        {'q0':[('0',{'q1','q2'}),('1',{'q0'}),(n.epsilon(),{'q2'})],
        'q1':[('0',{'q1'}),('1',{'q2'})]
        }
    )
    print(n.deltas())
    print(n.run(''))
    n.draw()
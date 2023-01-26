import os
import sys
import copy
from typing import List,Dict,Tuple
from graphviz import Digraph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automata.DFA import DFA
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

    def epsilon(self)->str:
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

    def __move(self,states:set[str],c:str,report:bool = True):
        """Change states according to current states 'states' and letter 'c'

        Args:
            states (set[str]): pre_states
            ch (str): letter\n
            report (bool):
                True: raise when no conversion rule is found.
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
                    

    def __epsilon_closure(self,states:set[str])->set:
        """Find the Epsilon closure of the states set.

        Args:
            states (set[str]): states set

        Returns:
            set: epsilon closure of the states set
        """
        result = states.copy()
        st = list(states.copy())
        while len(st)>0:
            top = st.pop()
            if top not in self.__deltas.keys():
                continue
            else:
                for (ch,next_states) in self.__deltas[top]:
                    if ch == self.__epsilon:
                        result |= next_states
                        for state in next_states:
                            if state not in st:
                                st.append(state)
            
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
    
    def to_DFA(self)->DFA:
        """Construct DFA equivalent to NFA by subset construction method.

        Returns:
            DFA: DFA object returned.
        """
        d = DFA()
        new_state_idx = 0
        # Dstates: [pre_states_set, new_state_name, mark]
        Dstates = []
        Dtrans = dict() # new transition
        Dstates.append([
        sorted(
            list(
                self.__epsilon_closure({self.__q0})
                )
            ),
        f's{new_state_idx}',
        False])
        new_state_idx += 1
        all_marked = False
        unmarked_Dstate_T_idx = 0 # Call this unmarked state 'T'.
        while all_marked == False:
            # Update the mark.
            all_marked = True
            
            # Find the first unmarked Dstate.
            for i in range(0,len(Dstates)):
                if Dstates[i][2] == False:
                    unmarked_Dstate_T_idx = i
                    all_marked = False
                    break
            
            # Mark the Dstate unmarked
            Dstates[unmarked_Dstate_T_idx][2] = True
            
            # for transition use
            T_name = Dstates[unmarked_Dstate_T_idx][1]
            U_name = None

            # Find the next transition state U of the state on each character
            for ch in self.__alphabet:
                state_U =sorted(
                    list(
                    self.__epsilon_closure(
                        self.__move(set(Dstates[unmarked_Dstate_T_idx][0]),ch,report=False))
                        )
                )
                # If the new state is not in DStates, add it.
                U_idx = -1
                for i in range(0,len(Dstates)):
                    if Dstates[i][0] == state_U:
                        U_idx = i
                        U_name = Dstates[i][1]
                        break
                

                if U_idx == -1:
                    U_name = f's{new_state_idx}'
                    Dstates.append([state_U,U_name,False])
                    new_state_idx += 1
                
                # Add the transition
                if T_name not in Dtrans:
                    Dtrans[T_name] = []
                Dtrans[T_name].append((ch,U_name))

        d.set_alphabet(self.__alphabet)
        for i in range(0,len(Dstates)):
            d.add_state(Dstates[i][1])
        if len(Dstates)>0:
            d.set_q0(Dstates[0][1])
        D_finish_states = []
        for i in range(0,len(Dstates)):
            for state in Dstates[i][0]:
                if state in self.__finish_states:
                    D_finish_states.append(Dstates[i][1])
        d.set_finish_states(D_finish_states)
        d.set_deltas(Dtrans)
        
        '''
        for it in Dstates:
            print(it)
        '''
        return d
    
    def clear(self):
        """ clear all info in NFA
        """
        self.__alphabet.clear()
        self.__Q.clear()
        self.__q0 = ''
        self.__deltas.clear()
        self.__finish_states.clear()
    
    def regex_to_NFA(self,regex:str,copy = False,to_dfa=False):
        """Construct NFA from regular expressions.

        Args:
            regex (str): basic regex (operators include '|', '*' '()'), end with '$'
            copy (bool, optional): if True, return a new NFA, else Generate in original NFA. Defaults to False.
            to_dfa (bool, optional): translate the generated NFA to DFA. Defaults to False.
        Return:
            NFA/DFA/None
        """
        def new_state(loc = 'right')->str:
            """Generate a new state.

            Args:
                loc (str, optional): state location. Defaults to 'right'.

            Returns:
                str: state string
            """
            nonlocal state_idx_left,state_idx_right,re_states
            state = None
            if loc == 'right':
                state = f'{state_idx_right}'
                re_states.append(state_idx_right)
                state_idx_right += 1
                
            elif loc == 'left':
                state = f'{state_idx_left}'
                re_states.append(state_idx_left)
                state_idx_left -= 1

            return state
    

        def add_trans(start:str,end:str,ch:str):
            """ Add transition to re_trans 

            Args:
                start (str): start_state
                end (str): end_state
                ch (str): character in alphabet or epsilon
            """
            nonlocal re_trans
            if start not in re_trans.keys():
                re_trans[start] = []
            for (c,next_states) in re_trans[start]:
                if c == ch:
                    next_states.add(end)
                    return
            re_trans[start].append((ch,{end}))
            return

        def is_operand(ch:str)->bool:
            """Judge if ch is a legal operand of the regex.

            Args:
                ch (str): ch with length of 1

            Returns:
                bool: result
            """
            if (ch>='0' and ch <='9') or\
                (ch >= 'a' and ch <='z') or\
                    (ch >='A' and ch <='Z'):
                    return True
            return False

        def infix_to_postfix(infix_exp:str)->str:
            """Convert infix_exp to postfix_exp.

            Args:
                infix_exp (str): ends with '$'

            Returns:
                postfix_exp
            """
            temp_str = ''
            # And the connector if necessary.
            for i in range(0,len(infix_exp)):
                ch = infix_exp[i]
                temp_str += ch
                if i < len(infix_exp)-1:
                    nextch = infix_exp[i+1]
                    if (is_operand(ch) and  nextch == '(') or \
                        (is_operand(ch) and is_operand(nextch)) or\
                            (ch == '*' and is_operand(nextch)) or \
                                (ch == '*' and nextch == '(') or \
                                    (ch == ')' and nextch == '('):
                        temp_str += '.'
            st = []
            postfix = ''
            for i in range(0,len(temp_str)):
                ch = temp_str[i]
                if is_operand(ch):
                    postfix += ch
                else:
                    if len(st) == 0:# st is empty
                        st.append(ch)
                    else:
                        if ch == '(':
                            st.append(ch)
                        elif ch == ')':
                            top = st[len(st)-1]
                            while(top != '('):
                                postfix += st.pop()
                                top = st[len(st)-1]
                            st.pop()
                        else:
                            top = st[len(st)-1]
                            if property_level[ch] <= property_level[top]:
                                while property_level[top] >= property_level[ch]:
                                        postfix += st.pop()
                                        if len(st) == 0:
                                            break
                                        else:
                                            top = st[len(st)-1]
                            st.append(ch)

            while len(st)!= 0:
                top = st[len(st)-1]
                if top != '(' and top!= ')':
                    postfix += top
                st.pop()
            return postfix

        def concat(start:str,end:str):
            """Generate transition for '.'

            Args:
                start (str): start state
                end (str): end state
            """
            add_trans(start,end,self.__epsilon)
            
        def union(start1:str,end1:str,start2:str,end2:str)->Tuple[str,str]:
            """Generate transition for NFA1 and NFA1 on '|'

            Args:
                start1 (str): start state of NFA1
                end1 (str): end state of NFA1
                start2 (str): start state of NFA2
                end2 (str): end state of NFA2
            
            Return:
                Tuple[str,str]: new_start, new_end
            """        
            # create a new start statex
            new_start = new_state('left')

            # add trans for new_start
            add_trans(new_start,start1,self.__epsilon)
            add_trans(new_start,start2,self.__epsilon)

            # create a new end state
            new_end = new_state('right')

            # add trans for new_start
            add_trans(end1,new_end,self.__epsilon)
            add_trans(end2,new_end,self.__epsilon)

            return (new_start,new_end)
        
        def closure(start:str,end:str)->Tuple[str,str]:
            """Generate transition of NFA on '*'

            Args:
                start (str): start state
                end (str): end state

            Returns:
                Tuple[str,str]: new_start, new_end
            """
            # create new start and new end
            nonlocal state_idx
            new_start = new_state('left')
            new_end = new_state('right')

            # add trans for new start and new end
            add_trans(new_start,start,self.__epsilon)
            add_trans(new_start,new_end,self.__epsilon)

            add_trans(end,start,self.__epsilon)

            add_trans(end,new_end,self.__epsilon)

            return (new_start,new_end)
        
        def trans_from_symbol(ch:str)->Tuple[str,str]:
            """Generate NFA from the symbol.

            Args:
                ch (str): a symbol in alphbet, or epsilon

            Returns:
                Tuple[str,str]: new_start, new_end
            """
            nonlocal state_idx
            new_start = new_state('right')
            new_end = new_state('right')

            add_trans(new_start,new_end,ch)
            return (new_start,new_end)

        if len(regex) == 0: # epsilon
            re_alphabet = set()
            re_states = ['s0','s1']
            re_trans = {
                's0':[(self.__epsilon,{'s1'})]
            }
            re_start = 's0'
            re_end = 's1'

        else:
            re_alphabet = set()
            re_trans = dict()
            re_states = []
            re_start = ''
            re_end = ''

            state_idx = 0
            state_idx_left = -1
            state_idx_right = 0
        
            property_level ={
                '(': 1,
                ')': 1,
                '|': 2,
                '.': 3,
                '*': 4
            }
            # Pre-check
            for ch in regex:
                if ch not in property_level.keys() and is_operand(ch) == False:
                    print(f'Illegal character \'{ch}\'')
                    return None
        
        
            # set alphabet:
            for ch in regex:
                if is_operand(ch):
                    re_alphabet.add(ch)

            # generate NFA
            postfix_exp = infix_to_postfix(regex)
            st = [] # stack of NFA, format: [start_state,end_state]
            for ch in postfix_exp:
                if is_operand(ch):
                    (start,end) = trans_from_symbol(ch)
                    st.append((start,end))
                elif ch == '*':
                    (start,end) = st.pop()
                    (start,end) = closure(start,end)
                    st.append((start,end))
                elif ch == '.':
                    (start2,end2) = st.pop()
                    (start1,end1) = st.pop()
                    concat(end1,start2)
                    st.append((start1,end2))
                elif ch == '|':
                    (start1,end1) = st.pop()
                    (start2,end2) = st.pop()
                    (start,end) = union(start1,end1,start2,end2)
                    st.append((start,end))
        
            (start,end) = st.pop()
            re_start = start
            re_end = end

            # renumber states
            temp_trans = re_trans.copy()
            temp_states = sorted(re_states)
        
            re_trans.clear()
            re_states.clear()

            idx_base = temp_states[0]
            for temp_idx in temp_states:
                new_idx = temp_idx - idx_base
                re_states.append(f's{new_idx}')
                re_trans[f's{new_idx}'] = []
                if f'{temp_idx}' not in temp_trans.keys():
                    continue
                else:
                    for (c,next_states) in temp_trans[f'{temp_idx}']:
                        renumber_next_states = set()
                        for next_state in next_states:
                            renumber_next_states.add(f's{int(next_state)-idx_base}')
                        re_trans[f's{new_idx}'].append((c,renumber_next_states))
        
            re_start = f's{int(re_start)-idx_base}'
            re_end = f's{int(re_end)-idx_base}'

        if copy == False:
            self.clear()
            self.set_alphabet(re_alphabet)
            self.set_alphabet(re_alphabet)
            self.add_states(re_states)
            self.set_q0(re_start)
            self.set_finish_states([re_end])
            self.set_deltas(re_trans)
            if to_dfa == True:
                self.to_DFA()
            return None
        else:
            n = NFA()
            n.set_alphabet(re_alphabet)
            n.add_states(re_states)
            n.set_q0(re_start)
            n.set_finish_states([re_end])
            n.set_deltas(re_trans)
            if to_dfa == True:
                n.to_DFA()
            return n        
        pass

    def __str__(self) -> str:
        return f"States   : {self.__Q} \n"\
               f"Alphabet : {self.__alphabet}\n"\
               f"Q0       : {self.__q0}\n"\
               f"Deltas   : {self.__deltas}\n"\
               f"Finish   : {self.__finish_states}\n"\
               f"Epsilon  : {self.__epsilon}"


if __name__ == '__main__':
    pass


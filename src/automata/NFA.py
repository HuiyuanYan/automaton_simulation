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
        self.__alphabet = set()
        self.__deltas = dict()
        self.__q0 = '' # start state
        self.__finish_states = set() # finish state
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
    
    def set_finish_states(self,finish_states:set[str]):
        '''
        Set finish states for NFA.
        '''
        for f in finish_states:
            try:
                if f in self.__Q:
                    if f not in self.__finish_states:
                        self.__finish_states.add(f)
                else:
                    raise NoneexistentStateException(f)
            except NoneexistentStateException as e:
                self.__finish_states.clear()
                sys.stderr.write(e.__str__()+'\n')
                return
    
    def set_alphabet(self,alphabet:set[str]):
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
                        self.__alphabet.add(letter)
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
    def draw(self,name = 'NFA',path:str = default_save_path):
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
            if len(label)>1:
                label_list = label.split(',')
                label_list.sort()
                label = ''
                for l in label_list:
                    if len(label) == 0:
                        label += l
                    else:
                        label += f',{l}'
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
        D_finish_states = set()
        for i in range(0,len(Dstates)):
            for state in Dstates[i][0]:
                if state in self.__finish_states:
                    D_finish_states.add(Dstates[i][1])
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
    
    def regex_to_NFA(self,regex:str,new_copy = False,to_dfa=False):
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


        def infix_to_postfix(infix_exp:str)->List[Tuple[str,int]]:
            """Convert infix_exp to postfix_exp.

            Args:
                infix_exp (str)

            Returns:
                postfix_exp
            """
            nonlocal OPERAND,OPERATOR,IN_SET
            property_level ={
                '(': 1,
                ')': 1,
                '[': 1,
                ']': 1,
                '|': 2,
                '.': 3,
                '*': 4,
                '+': 4,
                '@': 5
            }
            custom_operator = {'.','@'} # for intermediate operation, not for regex expression
            def if_connected(attr,ch,next_attr,next_ch)->bool:
                if attr == OPERAND and  ((next_ch == '(' or next_ch == '[')and next_attr == OPERATOR):
                    return True
                elif attr == OPERAND and next_attr == OPERAND:
                    return True
                elif ((ch == '*' or ch == '+') and attr == OPERATOR) and next_attr == OPERAND:
                    return True
                elif ((ch == '*' or ch == '+') and attr == OPERATOR) and ((next_ch == '(' or next_ch == '[') and next_attr == OPERATOR):
                    return True
                elif ((ch == ')' or ch == ']') and attr == OPERATOR) and ((next_ch == '(' or next_ch == '[') and next_attr == OPERATOR):
                    return True
                elif ((ch == ')' or ch == ']') and attr == OPERATOR) and next_attr == OPERAND:
                    return True
                else:
                    return False
                pass
            
            def process_slash(pre_ch_attr):
                ch_attr = []
                for i in range(0,len(pre_ch_attr)):
                    ch = pre_ch_attr[i][0]
                    if i > 0 and pre_ch_attr[i-1][0] == '\\':
                        continue
                    if ch == '\\':
                        if i < len(pre_ch_attr)-1:
                            ch_attr.append((pre_ch_attr[i+1][0],OPERAND))
                        continue
                    if ch in property_level and ch not in custom_operator:
                        ch_attr.append((ch,OPERATOR))
                    else:
                        ch_attr.append((ch,OPERAND))
                return ch_attr

            def process_character_set(pre_ch_attr):
                # Check if character_set's formate is correct.
                mark = 0
                for ch ,attr in pre_ch_attr:
                    if ch == '[' and attr == OPERATOR:
                        mark = 1
                    if ch == ']' and attr == OPERATOR:
                        if mark == 1:
                            mark = 0
                if mark != 0:
                    exit(-1)
                
                # Process set.
                ch_attr = []
                for i in range(0,len(pre_ch_attr)):
                    ch = pre_ch_attr[i][0]
                    attr = pre_ch_attr[i][1]
                    if ch == '[' and attr == OPERATOR:
                        mark = 1
                        ch_attr.append((ch,attr))
                        continue
                    if ch == ']' and attr == OPERATOR:
                        mark = 0
                        ch_attr.append((ch,attr))
                        ch_attr.append(('@',OPERATOR))
                        continue
                    if mark == 0:
                        ch_attr.append((ch,attr))
                    elif mark == 1:
                        if ch == '-' and pre_ch_attr[i-1][0] != '['and pre_ch_attr[i+1][0] != ']':
                            ch_begin = pre_ch_attr[i-1][0]
                            ch_end = pre_ch_attr[i+1][0]
                            # pop ch_begin
                            ch_attr.pop()

                            # push ch between ch_begin and ch_end
                            for ch_idx in range(ord(ch_begin),ord(ch_end)):
                                ch_attr.append((chr(ch_idx),IN_SET))
                            
                        else:
                            ch_attr.append((ch,IN_SET))
                return ch_attr
            
            def process_connection(pre_ch_attr):
                ch_attr = []
                for i in range(0,len(pre_ch_attr)):
                    ch = pre_ch_attr[i][0]
                    attr = pre_ch_attr[i][1]
                    ch_attr.append(pre_ch_attr[i])
                    if i < len(pre_ch_attr)-1:
                        next_ch = pre_ch_attr[i+1][0]
                        next_attr = pre_ch_attr[i+1][1]
                        if if_connected(attr,ch,next_attr,next_ch) == True:
                            ch_attr.append(('.',OPERATOR))
                return ch_attr
            
            # Preprocess infix_exp.
            ch_attr = [(c,0)for c in infix_exp]
            ch_attr = process_slash(ch_attr)
            
            ch_attr = process_character_set(ch_attr)
            
            ch_attr = process_connection(ch_attr)
            
            
            st = []
            postfix_ch_attr = []
            for i in range(0,len(ch_attr)):
                ch = ch_attr[i][0]
                attr = ch_attr[i][1]
                if attr == OPERAND or attr == IN_SET:
                    postfix_ch_attr.append((ch,attr))
                elif attr == OPERATOR:
                    if len(st) == 0:# st is empty
                        st.append(ch)
                    else:
                        if ch == '(':
                            st.append(ch)
                        elif ch == ')':
                            top = st[len(st)-1]
                            while(top != '('):
                                postfix_ch_attr.append((st.pop(),OPERATOR))
                                top = st[len(st)-1]
                            st.pop()
                        elif ch == '[':
                            st.append(ch)
                        elif ch == ']':
                            top = st[len(st)-1]
                            while(top != '['):
                                postfix_ch_attr.append((st.pop(),OPERATOR))
                                top = st[len(st)-1]
                            st.pop()
                        else:
                            top = st[len(st)-1]
                            if property_level[ch] <= property_level[top]:
                                while property_level[top] >= property_level[ch]:
                                        postfix_ch_attr.append((st.pop(),OPERATOR))
                                        if len(st) == 0:
                                            break
                                        else:
                                            top = st[len(st)-1]
                            st.append(ch)

            while len(st)!= 0:
                top = st[len(st)-1]
                if top != '(' and top!= ')':
                    postfix_ch_attr.append((top,OPERATOR))
                st.pop()
            return postfix_ch_attr

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
        
        def plus(start:str,end:str)->Tuple[str,str]:
            """Generate transition of NFA on '+'

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

            add_trans(end,start,self.__epsilon)

            add_trans(end,new_end,self.__epsilon)

            return (new_start,new_end)
            pass

        def trans_from_symbol(ch_set:set[str])->Tuple[str,str]:
            """Generate NFA from the symbol.

            Args:
                ch (str): a symbol in alphbet, or epsilon

            Returns:
                Tuple[str,str]: new_start, new_end
            """
            nonlocal state_idx
            new_start = new_state('right')
            new_end = new_state('right')
            for ch in ch_set:
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
            OPERAND = 0
            OPERATOR = 1
            IN_SET = 2
    
            re_alphabet = set()
            re_trans = dict()
            re_states = []
            re_start = ''
            re_end = ''

            state_idx = 0
            state_idx_left = -1
            state_idx_right = 0
    
            # get postfix_ch_attr 
            postfix_ch_attr = infix_to_postfix(regex)
            
            """
            postfix_exp = ''.join(c for c,a in postfix_ch_attr)
            print(postfix_exp)
            """

            # generate NFA
            
            st = [] # stack of NFA, format: [start_state,end_state]
            tmp_alphabet_list = []
            for ch,attr in postfix_ch_attr:
                if attr == OPERAND:
                    (start,end) = trans_from_symbol({ch})
                    # set alphabet:
                    re_alphabet.add(ch)
                    st.append((start,end))
                elif attr == OPERATOR:
                    if ch == '*':
                        (start,end) = st.pop()
                        (start,end) = closure(start,end)
                        st.append((start,end))
                    elif ch == '+':
                        (start,end) = st.pop()
                        (start,end) = plus(start,end)
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
                    elif ch == '@':
                        # set alphabet:
                        for c in tmp_alphabet_list:
                            re_alphabet.add(c)

                        (start,end) = trans_from_symbol(set(tmp_alphabet_list))
                        st.append((start,end))
                        tmp_alphabet_list.clear()
                elif attr == IN_SET:
                    tmp_alphabet_list.append(ch)
        
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

        if new_copy == False:
            self.clear()
            self.set_alphabet(re_alphabet)
            self.set_alphabet(re_alphabet)
            self.add_states(re_states)
            self.set_q0(re_start)
            self.set_finish_states({re_end})
            self.set_deltas(re_trans)
            if to_dfa == True:
                self.to_DFA()
            return None
        else:
            n = NFA()
            n.set_alphabet(re_alphabet)
            n.add_states(re_states)
            n.set_q0(re_start)
            n.set_finish_states({re_end})
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


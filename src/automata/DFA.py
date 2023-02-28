import os
import sys
import copy
from graphviz import Digraph
from typing import List,Dict,Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automata.config import default_save_path
from container import disjoint_set as ds
from automata.myException import DuplicateStateException,NoneexistentStateException,NoneexistentLetterException,\
    IncorrectLetterlLengthException,NonexistentTransitionRule


class DFA:
    def __init__(self):
        self.__Q = [] # states
        self.__alphabet = set()
        self.__deltas = dict()
        self.__q0 = '' # start state
        self.__finish_states = set() # finish state
        pass

    def add_state(self,state:str):
        '''
        Add a transition state to DFA.
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
        Add states to DFA.
        '''
        for state in states:
            self.add_state(state)
    
    def set_q0(self,q0:str):
        '''
        Set start states for DFA.
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
        Set finish states for DFA.
        '''
        self.__finish_states.clear()
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
        Set alphabet for DFA.
        '''
        self.__alphabet.clear()
        for letter in alphabet:
            try:
                if len(letter) != 1:
                    raise IncorrectLetterlLengthException(letter)
                else:
                    if letter not in self.__alphabet:
                        self.__alphabet.add(letter)
            except IncorrectLetterlLengthException as e:
                self.__alphabet.clear()
                sys.stderr.write(e.__str__()+'\n')
                return

    def add_delta(self,src:str,letter:str,target:str):
        '''
        Set transition for DFA.
        '''
        try:
            if src not in self.__Q:
                raise NoneexistentStateException(src)
            if letter not in self.__alphabet:
                raise NoneexistentLetterException(letter)
            if target not in self.__Q:
                raise NoneexistentStateException(target)
            
            if src not in self.__deltas:
                self.__deltas[src] = []
            if (letter,target) not in self.__deltas[src]:
                self.__deltas[src].append((letter,target)) 
        except NoneexistentStateException as e:
            sys.stderr.write(e.__str__()+'\n')
        except NoneexistentLetterException as e:
            sys.stderr.write(e.__str__()+'\n')
        return

    def set_deltas(self,deltas:Dict[str,List[Tuple[str,str]]]):
        '''
        Set transitions for DFA.
        deltas: Set of transitions.
        transtion format: (src,(letter,target))
        '''
        self.__deltas.clear()
        for key,value in deltas.items():
            for (letter,next) in value:
                self.add_delta(key,letter,next)
        return
    
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

    def __move(self,s:str,c:str):
        """Change state according to current state 's' and letter 'c'

        Args:
            s (str): current state
            c (str): letter
        Return: 
            next state / None: error
        """
        try:
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

        try:
            if s not in self.__deltas:
                raise NonexistentTransitionRule(s,c)
            for (letter,next) in self.__deltas[s]:
                if c == letter:
                    return next
            raise NonexistentTransitionRule(s,c)
        except NonexistentTransitionRule as e:
            sys.stderr.write(e.__str__()+'\n')
            return None

    def run(self,input:str,verbose = False)->bool:
        """Simulate input string on DFA.

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
        
        current_state = self.__q0
        for i in range(0,len(input)):
            if verbose == True:
                print(f'Pre    : {current_state}')
                print(f'Input  : {input}')
                print(f'Read   : '+i*' '+'^')
            current_state = self.__move(current_state,input[i])
            if current_state is None:
                return False
            if verbose == True:
                print(f'Next   : {current_state}\n')

        if current_state in self.__finish_states:
            return True
        else:
            return False

    def draw(self,name = 'DFA',path:str = default_save_path):
        """Draw picture for DFA.

        Args:
            name (str, optional): dest file name. Defaults to 'DFA'.
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
            for (letter,next) in val:
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
    
    def __split(self,s1:str,s2:str,table:List[List[int]])->bool:
        """Check whether s1 and s2 can be distinguished.

        Args:
            s1 (str): state1
            s2 (str): state2
            table (List[List[int]]): distinction table

        Returns:
            bool: True/False
        """
        for ch in self.__alphabet:
            next1 = None
            next2 = None
            for (letter,next) in self.__deltas[s1]:
                if letter == ch:
                    next1 = next
                    break
            for (letter,next) in self.__deltas[s2]:
                if letter == ch:
                    next2 = next
            if (next1 == None and next2 != None) or (next1 != None and next2 == None):
                return True
            if table[self.__Q.index(next1)][self.__Q.index(next2)] == 1 or table[self.__Q.index(next2)][self.__Q.index(next1)] == 1:
                return True
        return False 

    def minimize(self,new_copy = False):
        """Minimize DFA

        Args:
            new_copy (bool, optional): 

            If it is true, the function returns a new minimized DFA without modifying the original DFA;

            If it is false, the function modifies the original DFA to the minimized DFA and returns None. 
            
            Defaults to False.
        """
        def remove_unreachable_states():
            """Remove unreachable states of DFA
            """
            st = []
            visit = []
            st.append(self.__q0)
            while len(st)!= 0:
                top = st.pop()
                if top not in visit:
                    visit.append(top)
                if top in self.__deltas.keys():
                    for (ch,next) in self.__deltas[top]:
                        if next not in visit:
                            st.append(next)
            
            # remove transition
            for key in list(self.__deltas.keys()):
                if key not in visit:
                    del self.__deltas[key]
            self.__Q = sorted(visit.copy())
        

        remove_unreachable_states()
        states_num = len(self.__Q)
        table = [[0]*states_num for _ in range(states_num)]
        # Initialize
        for i in range(0,len(self.__Q)):
            if self.__Q[i] in self.__finish_states:
                for j in range(0,i):
                    if self.__Q[j] not in self.__finish_states:
                        table[i][j] = 1 #x
                for k in range(i+1,states_num):
                    if self.__Q[k] not in self.__finish_states:
                        table[k][i] = 1 #x
        
        updated = False
        while 1:
            updated = False
            for j in range(0,states_num-1):
                for i in range(j+1,states_num):
                    if table[i][j] == 1:
                        continue
                    else:
                        split = self.__split(self.__Q[i],self.__Q[j],table)
                        if split == True:
                            table[i][j] = 1
                            updated = True
            if updated == False:
                break

        d = ds.DisjointSet(self.__Q)
        for j in range(0,states_num-1):
            for i in range(j+1,states_num):
                if table[i][j] == 0:
                    d.union(self.__Q[i],self.__Q[j])
        
        set_list = d.get_set_list()

        # Redesign DFA
        new_Q = [f'q{i}'for i in range(0,len(set_list))]
        new_q0 = ''
        new_finsih_states = set()
        new_deltas = {}
        for l in set_list:
            if self.__q0 in l:
                new_q0 = f'q{set_list.index(l)}'
                break
        
        for l in set_list:
            for f in self.__finish_states:
                if f in l:
                    new_finsih_states.add(f'q{set_list.index(l)}')
        
        for (pre,deltas) in self.__deltas.items():
            for (letter,next) in deltas:
                new_pre = None
                new_next = None
                for l in set_list:
                    if pre in l:
                        new_pre = f'q{set_list.index(l)}'
                    if next in l:
                        new_next = f'q{set_list.index(l)}'
                assert new_pre != None and new_next != None
                if new_pre not in new_deltas.keys():
                    new_deltas[new_pre] = []
                
                exist = False
                for (temp_letter,temp_next) in new_deltas[new_pre]:
                    if temp_letter == letter:
                        exist = True
                        break
                if exist == False:
                    new_deltas[new_pre].append((letter,new_next))

        if new_copy == True:
            new_DFA = DFA()
            new_DFA.set_alphabet(self.__alphabet)
            new_DFA.add_states(new_Q)
            new_DFA.set_q0(new_q0)
            new_DFA.set_finish_states(new_finsih_states)
            new_DFA.set_deltas(new_deltas)
            return new_DFA
        else:
            self.__Q = new_Q
            self.__q0 = new_q0
            self.__finish_states = new_finsih_states
            self.__deltas = new_deltas
            return None

    def to_regex(self)->str:
        """Generate regular expressions corresponding to the DFA.

        Returns:
            str: regular expressions
        """
        def generate_re(i,j,k)->str:
            R_ij = re_matrix[i][j]
            R_ik = re_matrix[i][k]
            R_kk = re_matrix[k][k]
            R_kj = re_matrix[k][j]
            
            if len(R_ik) > 1:
                R_ik = f'({R_ik})'
            if len(R_kj) > 1:
                R_kj = f'({R_kj})'

            ret = R_ij
            if len(R_ik) == 0 or len(R_kk) == 0 or len(R_kj) == 0:
                return ret
            else:
                if len(R_ij) == 0:
                    ret = f'{R_ik}({R_kk})*{R_kj}'
                else:
                    ret = R_ij + '+' f'{R_ik}({R_kk})*{R_kj}'
            return ret

        epsilon = 'ε'
        states_num = len(self.__Q)
        re_matrix = [[''for i in range(0,states_num)]for j in range(0,states_num)]

        for i in range(0,states_num):
            for j in range(0,states_num):
                state_i = self.__Q[i]
                state_j = self.__Q[j]
                if i == j:
                    re_matrix[i][j] += epsilon
                    for (ch,next) in self.__deltas[state_i]:
                        if next == state_i:
                            re_matrix[i][j] += f'+{ch}'
                else:        
                    first = True
                    if state_i in self.__deltas.keys():
                        for (ch,next) in self.__deltas[state_i]:
                            if next == state_j:
                                if first == True:
                                    re_matrix[i][j] += f'{ch}'
                                    first = False
                                else:
                                    re_matrix[i][j] += f'+{ch}'
        
        for k in range(0,states_num):
            # print(re_matrix)
            temp_matrix = [[''for i in range(0,states_num)]for j in range(0,states_num)]
            for i in range(0,states_num):
                for j in range(0,states_num):
                    temp_matrix[i][j] = generate_re(i,j,k)
            re_matrix = temp_matrix.copy()
        # print(re_matrix)

        ret = ''
        start_idx = self.__Q.index(self.__q0)
        first = True
        for finish_state in self.__finish_states:
            idx = self.__Q.index(finish_state)
            if first == True:
                ret += re_matrix[start_idx][idx]
                first = False
            else:
                ret += f'+{re_matrix[start_idx][idx]}'
        return ret

    def is_empty(self)->bool:
        """Test whether the DFA/regular accepted language is empty(Ø).

        Note that "empty" here refers to not accepting any language, which is different from the epsilon.
        
        Returns:
            bool: result
        """
        # Check whether the finish states are reachable, if there is a finish state is reachable, return True.
        # method: DFS
        st = []
        visit = set()
        st.append(self.__q0)
        while len(st)!= 0:
            top = st.pop()
            visit.add(top)
            if top in self.__deltas:
                for ch,next in self.__deltas[top]:
                    if next not in visit:
                        st.append(next)
        for state in self.__finish_states:
            if state in visit:
                return False
        return True

    def is_equal(self,other)->bool:
        """Determines whether the languages accepted by the two Dfas are equivalent.

        Args:
            other (DFA): a DFA

        Returns:
            bool: result

        Method: Product DFA.

        F = set({q1,q2}), where q1 is in F1 and q2 is not in F2, or q1 is not in F1 and q2 is in F2.

        If the language accepted by 'ap' is empty, then L(a1) = L(a2).
        
        If not, then L(a1) = L(a2).

        This can be checked traversing the state transitions of the DFA.
        """
        ap = self.__caculate_product_dfa(self,other)

        f1 = self.finish_states()
        f2 = other.finish_states()
        ap_finish = set()
        for q in ap.Q():
            q1,q2 = q.split(',')
            if q1 in f1 and q2 not in f2:
                ap_finish.add(f'{q1},{q2}')
            elif q1 not in f1 and q2 in f2:
                ap_finish.add(f'{q1},{q2}')
                
        
        ap.set_finish_states(ap_finish)
        if ap.is_empty():
            #Also, There must be a path from the beginning to the acceptance of both DFAs.
            st = [ap.q0()]
            vis = set()
            ap_trans = ap.deltas()
            while len(st) > 0:
                q = st[len(st)-1]
                st.pop()
                vis.add(q)
                if q in ap_trans:
                    for ch,p in ap_trans[q]:
                        if p not in vis:
                            st.append(p)
            for s in vis:
                q0,q1 = s.split(',')
                if q0 in f1 and q1 in f2:
                    return True
            return False
        else:
            return False

    def __caculate_product_dfa(self,a1,a2):
        """Caculate the product of two DFAs, without setting finish states.

        Args:
            other (DFA): a dfa.
        
        For DFA a1 and a2, generate the product DFA ap like this:

        ∑ = ∑1 | ∑2

        Q = {Q1 x Q2}, cartesian product of two sets of states.
        
        δ({q1,q2},c) = ({p1,p2}) ,where δ1(q1,c)=p1, δ2(q2,c)=p2.

        q0 = {q0_1, q0_2}
        """
        ap = DFA() # product DFA
        ap.set_alphabet(a1.alphabet() | a2.alphabet())
        ap_states = []


        Q1 = a1.Q()
        Q2 = a2.Q()

        deltas1 = a1.deltas()
        deltas2 = a2.deltas()

        for q1 in Q1:
            for q2 in Q2:
                ap_states.append(f'{q1},{q2}')
        


        ap.add_states(ap_states)
        ap.set_q0(f'{a1.q0()},{a2.q0()}')
        
        for s in ap_states:
            q1,q2 = s.split(',')
            if q1 not in deltas1 or q2 not in deltas2:
                continue
            for t1 in deltas1[q1]:
                ch1 = t1[0]
                p1 = t1[1]
                for t2 in  deltas2[q2]:
                    ch2 = t2[0]
                    p2 = t2[1]
                    if ch1 == ch2:
                        ap.add_delta(
                            f'{q1},{q2}',
                            ch1,
                            f'{p1},{p2}'
                        )
        return ap

    def intersection(self,other):
        """Caculate the intersection of two DFAs.

        Args:
            other (DFA): a dfa.
        """
        
        alphabet = self.__alphabet | other.alphabet()
        f1 = self.__finish_states
        f2 = other.finish_states()

        a1 = self.complement_transitions(self,alphabet,_copy =True)
        a2 = other.complement_transitions(other,alphabet,_copy = True)
        
        ap = self.__caculate_product_dfa(a1,a2)
    
        f1 = self.finish_states()
        f2 = other.finish_states()
        ap_finish = set()
        for s in ap.Q():
            q1,q2 = s.split(',')
            if q1 in f1 and q2 in f2:
                ap_finish.add(s)
        ap.set_finish_states(ap_finish)
        ap.minimize()
        return ap

    
    def union(self,other):
        """Caculate the union of two DFAs.

        Args:
            other (DFA): a dfa.
        """
        alphabet = self.__alphabet | other.alphabet()
        f1 = self.__finish_states
        f2 = other.finish_states()

        a1 = self.complement_transitions(self,alphabet,_copy =True)
        a2 = other.complement_transitions(other,alphabet,_copy = True)
        
        ap = self.__caculate_product_dfa(a1,a2)
        ap_finish = set()
        for q in ap.Q():
            q1,q2 = q.split(',')
            if q1 in f1 or q2 in f2:
                ap_finish.add(q)
        ap.set_finish_states(ap_finish)
        ap.minimize()
        return ap

        


    def complement_transitions(self,a,alphabet,_copy = False):
        """Complement the transitions in alphabet.

        Args:
            a (DFA): DFA a.
            
            copy (bool): If true, return a new copy.
        """
        alphabet_copy = copy.deepcopy(alphabet)
        old_copy = None
        if _copy == True:
            old_copy = copy.deepcopy(a)
        
        delta = a.deltas()
        a.set_alphabet(alphabet_copy)
        states = a.Q()
        dead_state = ''
        for q in states:
            ch_list = copy.deepcopy(alphabet_copy)
            if q in delta:
                for ch,p in delta[q]:
                    ch_list.remove(ch)
            if len(ch_list) != 0:
                if len(dead_state) == 0:
                    dead_state = 'q_dead'
                    a.add_state(dead_state)
                    for c in alphabet_copy:
                        a.add_delta(
                            dead_state,
                            c,
                            dead_state
                        )
                for ch in ch_list:
                    a.add_delta(
                        q,
                        ch,
                        dead_state
                    )
        if _copy == True: 
            # restore the original DFA 'a' and return a new copy
            ret = copy.deepcopy(a)
            a.clear()
            a.set_alphabet(old_copy.alphabet())
            a.add_states(old_copy.Q())
            a.set_deltas(old_copy.deltas())
            a.set_q0(old_copy.q0())
            a.set_finish_states(old_copy.finish_states())
            return ret
        return None

    def complement(self):
        """Caculate the complement of DFA.
        """
        a = self.complement_transitions(self,self.__alphabet, _copy = True)
        states = a.Q()
        finish = a.finish_states()
        deltas = a.deltas()

        ac = DFA()
        ac_states = [f'q{i}'for i in range(0,len(states))]
        ac_q0 = f'q{states.index(a.q0())}'
        ac_finish = set()

        for q in states:
            if q not in finish:
                ac_finish.add(f'q{states.index(q)}')

        ac.set_alphabet(self.__alphabet)
        ac.add_states(ac_states)
        ac.set_q0(ac_q0)
        ac.set_finish_states(ac_finish)

        for q in states:
            if q in deltas:
                for ch,p in deltas[q]:
                    ac.add_delta(
                        f'q{states.index(q)}',
                        ch,
                        f'q{states.index(p)}'
                    )
        return ac

    def difference(self,other):
        """Caculate the difference of two DFAs.

        Args:
            other (DFA): a dfa.
        """
        alphabet = self.__alphabet | other.alphabet()
        f1 = self.__finish_states
        f2 = other.finish_states()

        a1 = self.complement_transitions(self,alphabet,_copy =True)
        a2 = other.complement_transitions(other,alphabet,_copy = True)
        
        ap = self.__caculate_product_dfa(a1,a2)

        ap_finish = set()
        
        for s in ap.Q():
            q1,q2 = s.split(',')
            if q1 in f1 and q2 not in f2:
                ap_finish.add(s)
        ap.set_finish_states(ap_finish)
        ap.minimize()
        return ap


    def __str__(self) -> str:
        return f"States   : {self.__Q} \n"\
               f"Alphabet : {self.__alphabet}\n"\
               f"Q0       : {self.__q0}\n"\
               f"Deltas   : {self.__deltas}\n"\
               f"Finish   : {self.__finish_states}\n"
    
    def clear(self):
        """Clear All info of DFA
        """
        self.__alphabet.clear()
        self.__deltas.clear()
        self.__finish_states.clear()
        self.__Q.clear()
        self.__q0 = ''

if __name__ == '__main__':
    pass
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.automata.PDA import PDA_F,PDA_E

def test_PDA_F():
    a = PDA_F()
    a.set_input_symbols({'0','1'})
    a.set_pushdown_symbols({'0','1','Z'})
    a.add_states(['q0','q1','q2'])
    a.set_initial_state('q0')
    a.set_initial_symbol('Z')
    a.set_finish_states({'q2'})
    a.add_transition('q0','0','Z','q1','Z0')
    a.add_transition('q1','1','0','q2','01')
    # a.draw()
    assert a.run('01') == True
    assert a.run('001') == False
    print(a)
    pass

def test_PDA_E():
    a = PDA_E()
    a.set_input_symbols({'0','1'})
    a.set_pushdown_symbols({'0','1','Z'})
    a.add_states(['q0','q1'])
    a.set_initial_state('q0')
    a.set_initial_symbol('Z')
    a.add_transition('q0','0','Z','q0','Z0')
    a.add_transition('q0','0','0','q0','00')
    a.add_transition('q0','1','0','q1',a.epsilon())
    a.add_transition('q1','1','0','q1',a.epsilon())
    a.add_transition('q1',a.epsilon(),'Z','q1',a.epsilon())
    a.draw()
    assert a.run('01') == True
    assert a.run('001') == False
    assert a.run('0011') == True
    print(a)
    pass

if __name__ == '__main__':
    test_PDA_E()
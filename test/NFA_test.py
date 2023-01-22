import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.automata.NFA as NFA_SRC

def test_nfa1():
    n = NFA_SRC.NFA()
    n.set_alphabet(['0','1'])
    n.add_states(['q0','q1','q2'])
    n.set_q0('q0')
    n.set_finish_states(['q2'])
    n.set_deltas(
        {'q0':[('0',{'q1','q2'}),('1',{'q0'}),(n.epsilon(),{'q2'})],
        'q1':[('0',{'q1'}),('1',{'q2'})]
        }
    )
    assert n.run('') == True
    assert n.run('11') == True
    assert n.run('100') == False
    assert n.run('1001') == True

def test_all():
    test_nfa1()

if __name__ == '__main__':
    test_nfa1()
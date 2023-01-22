import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.automata.DFA as DFA_SRC
 


def test_dfa1():
    d = DFA_SRC.DFA()
    d.add_states(['q0','q1','q2','q3'])
    d.set_alphabet(['0','1'])
    d.set_q0('q0')
    d.set_finish_states(['q3'])
    d.set_deltas({'q0':[('0','q1')],
                  'q1':[('1','q2')],
                  'q2':[('0','q3')],
    })

    assert d.run('0') == False
    assert d.run('01') == False
    assert d.run('010') == True

def test_minimize():
    d = DFA_SRC.DFA()
    d.set_alphabet(['0','1'])
    d.add_states(['A','B','C','D','E','F','G','H'])
    d.set_q0('A')
    
    d.set_finish_states(['C'])
    d.set_deltas(
        {
            'A':[('0','B'),('1','F')],
            'B':[('0','G'),('1','C')],
            'C':[('0','A'),('1','C')],
            'D':[('0','C'),('1','G')],
            'E':[('0','H'),('1','F')],
            'F':[('0','C'),('1','G')],
            'G':[('0','G'),('1','E')],
            'H':[('0','G'),('1','C')]
        }
    )
    new_d = d.minimize(new_copy=True)

    assert len(new_d.Q()) == 5
    assert d.run('01') == new_d.run('01')
    assert d.run('10') == new_d.run('10')
    assert d.run('010') == new_d.run('010')

def test_all():
    test_dfa1()
    test_minimize()

if __name__ == '__main__':
    test_dfa1()
    test_minimize()

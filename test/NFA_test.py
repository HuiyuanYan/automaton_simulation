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

def test_to_DFA():
    n = NFA_SRC.NFA()
    n.set_alphabet(['a','b'])
    n.add_states(['0','1','2','3','4','5','6','7','8','9','10'])
    n.set_q0('0')
    n.set_finish_states(['10'])
    n.set_deltas(
        {
            '0':[(n.epsilon(),{'1','7'})],
            '1':[(n.epsilon(),{'2','4'})],
            '2':[('a',{'3'})],
            '3':[(n.epsilon(),{'6'})],
            '4':[('b',{'5'})],
            '5':[(n.epsilon(),{'6'})],
            '6':[(n.epsilon(),{'1','7'})],
            '7':[('a',{'8'})],
            '8':[('b',{'9'})],
            '9':[('b',{'10'})]
        }
    )
    #n.draw()
    d = n.to_DFA()
    #d.draw()
    assert n.run('abb') == True
    assert n.run('aabb') == True
    assert n.run('babb') == True
    assert n.run('abbabb') == True

    assert n.run('a') == False
    assert n.run('b') == False
    assert n.run('ab') == False
    
    pass

def test_regex_to_NFA():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('(a|b)*abb',copy = False)

    assert n.run('abb') == True
    assert n.run('aabb') == True
    assert n.run('babb') == True
    assert n.run('abbabb') == True

    assert n.run('a') == False
    assert n.run('b') == False
    assert n.run('ab') == False

    n.regex_to_NFA('',copy=False)
    assert n.run('') == True


def test_all():
    test_nfa1()
    test_to_DFA()
    test_regex_to_NFA()

if __name__ == '__main__':
    test_all()
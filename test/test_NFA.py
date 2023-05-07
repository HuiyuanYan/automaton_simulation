import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.automata.NFA as NFA_SRC

def test_nfa1():
    n = NFA_SRC.NFA()
    n.set_alphabet({'0','1'})
    n.add_states(['q0','q1','q2'])
    n.set_q0('q0')
    n.set_finish_states({'q2'})
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
    n.set_alphabet({'a','b'})
    n.add_states(['0','1','2','3','4','5','6','7','8','9','10'])
    n.set_q0('0')
    n.set_finish_states({'10'})
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

def test_regex_to_NFA1():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('(a|b)*abb',new_copy = False)

    assert n.run('abb') == True
    assert n.run('aabb') == True
    assert n.run('babb') == True
    assert n.run('abbabb') == True

    assert n.run('a') == False
    assert n.run('b') == False
    assert n.run('ab') == False

    n.regex_to_NFA('',new_copy=False)
    assert n.run('') == True

    n.regex_to_NFA('1*0(0|1)*',new_copy=False)
    d = n.to_DFA()
    d.minimize()
    assert len(d.Q()) == 2
    assert d.run('1110') == True
    assert d.run('1') == False
    assert d.run('111100001') == True

def test_regex_to_NFA2():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('(a|b)+',new_copy = False)
    d = n.to_DFA().minimize(new_copy = True)

def test_regex_to_NFA3():
    digit1 = '(1|2|3|4|5|6|7|8|9)'
    digit2 = '(0|1|2|3|4|5|6|7|8|9)'
    s = f'0|({digit1}{digit2}*)'
    n = NFA_SRC.NFA()
    n.regex_to_NFA(s,new_copy = False)
    d = n.to_DFA().minimize(new_copy = True)
    assert d.run('0') == True
    assert d.run('1') == True
    assert d.run('123') == True
    assert d.run('0123') ==False

def test_regex_to_NFA4():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('\\(',new_copy = False)
    d = n.to_DFA().minimize(new_copy = True)
    assert d.run('(') == True

def test_regex_to_NFA5():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('[a-z]+',new_copy = False)
    d = n.to_DFA().minimize(new_copy = True)
    for ch_idx in range(ord('a'),ord('z')+1):
        assert d.run(chr(ch_idx)) == True

def test_regex_to_NFA6():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('[.*+|-]',new_copy = False)
    d = n.to_DFA().minimize(new_copy = True)
    assert d.run('.') == True
    assert d.run('*') == True
    assert d.run('+') == True
    assert d.run('|') == True
    assert d.run('-') == True


def test_regex_to_NFA7():
    n = NFA_SRC.NFA()
    n.regex_to_NFA('[a-zA-Z_]+[a-zA-Z0-9_]*',new_copy = False)
    d = n.to_DFA().minimize(new_copy=True)
    assert d.run('0123') == False
    assert d.run('_a7') == True
    assert d.run('t0') == True

    d.draw()
def test_all():
    test_nfa1()
    test_to_DFA()
    test_regex_to_NFA1()
    test_regex_to_NFA2()
    test_regex_to_NFA3()
    test_regex_to_NFA4()
    test_regex_to_NFA5()
    test_regex_to_NFA6()
    test_regex_to_NFA7()


if __name__ == '__main__':
    test_regex_to_NFA7()
    
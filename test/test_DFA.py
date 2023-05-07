import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.automata.DFA as DFA_SRC
import src.automata.NFA as NFA_SRC


def test_dfa1():
    d = DFA_SRC.DFA()
    d.add_states(['q0','q1','q2','q3'])
    d.set_alphabet({'0','1'})
    d.set_q0('q0')
    d.set_finish_states({'q3'})
    d.set_deltas({'q0':[('0','q1')],
                  'q1':[('1','q2')],
                  'q2':[('0','q3')],
    })

    assert d.run('0') == False
    assert d.run('01') == False
    assert d.run('010') == True

def test_minimize():
    d = DFA_SRC.DFA()
    d.set_alphabet({'0','1'})
    d.add_states(['A','B','C','D','E','F','G','H'])
    d.set_q0('A')
    
    d.set_finish_states({'C'})
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

def test_to_regex():
    d = DFA_SRC.DFA()
    d.set_alphabet({'0','1'})
    d.add_states(['q0','q1'])
    d.set_q0('q0')
    d.set_finish_states({'q1'})
    d.set_deltas(
        {
            'q0':[('0','q1'),('1','q0')],
            'q1':[('0','q1'),('1','q1')]
        }
    )
    # print(d.to_regex())
    pass

def test_is_equal1():
    d1 = DFA_SRC.DFA()
    d1.set_alphabet({'a'})
    d1.add_states(['q0','q1'])
    d1.set_q0('q0')
    d1.set_finish_states({'q1'})
    d1.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )
    
    d2 = DFA_SRC.DFA()
    d2.set_alphabet({'b'})
    d2.add_states(['q0','q1'])
    d2.set_q0('q0')
    d2.set_finish_states({'q1'})
    d2.set_deltas(
        {
            'q0':[('b','q1')]
        }
    )

    assert d1.is_equal(d2) == False

def test_is_equal2():
    d1 = DFA_SRC.DFA()
    d1.set_alphabet({'a'})
    d1.add_states(['q0','q1'])
    d1.set_q0('q0')
    d1.set_finish_states({'q1'})
    d1.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )
    
    d2 = DFA_SRC.DFA()
    d2.set_alphabet({'a'})
    d2.add_states(['q0','q1'])
    d2.set_q0('q0')
    d2.set_finish_states({'q1'})
    d2.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )

    assert d1.is_equal(d2) == True

def test_is_equal3():
    d = DFA_SRC.DFA()
    d.set_alphabet({'0','1'})
    d.add_states(['A','B','C','D','E','F','G','H'])
    d.set_q0('A')
    
    d.set_finish_states({'C'})
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
    assert d.is_equal(new_d) == True
    pass

def test_complement1():
    d1 = DFA_SRC.DFA()
    d1.set_alphabet({'a'})
    d1.add_states(['q0','q1'])
    d1.set_q0('q0')
    d1.set_finish_states({'q1'})
    d1.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )
    d2 = d1.complement()
    assert d2.run('') == True
    assert d2.run('a') == False
    assert d2.run('aa') == True
    assert d2.run('aaa') == True

def test_complement2():
    n1 = NFA_SRC.NFA()
    n1.regex_to_NFA('(a|b)*')
    d1 = n1.to_DFA()
    d1.minimize()
    d2 = d1.complement()
    assert d2.is_empty() == True

def test_union():
    d1 = DFA_SRC.DFA()
    d1.set_alphabet({'a'})
    d1.add_states(['q0','q1'])
    d1.set_q0('q0')
    d1.set_finish_states({'q1'})
    d1.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )
    d2 = DFA_SRC.DFA()
    d2.set_alphabet({'b'})
    d2.add_states(['q0','q1'])
    d2.set_q0('q0')
    d2.set_finish_states({'q1'})
    d2.set_deltas(
        {
            'q0':[('b','q1')]
        }
    )
    d3 = d2.union(d1)
    assert d3.run('a') == True
    assert d3.run('b') == True

def test_intersection1():
    d1 = DFA_SRC.DFA()
    d1.set_alphabet({'a'})
    d1.add_states(['q0','q1'])
    d1.set_q0('q0')
    d1.set_finish_states({'q1'})
    d1.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )
    d2 = DFA_SRC.DFA()
    d2.set_alphabet({'b'})
    d2.add_states(['q0','q1'])
    d2.set_q0('q0')
    d2.set_finish_states({'q1'})
    d2.set_deltas(
        {
            'q0':[('b','q1')]
        }
    )
    d3 = d1.intersection(d2)
    assert d3.is_empty() == True
    pass

def test_intersection2():
    n1 = NFA_SRC.NFA()
    n1.regex_to_NFA('(a|b)*')
    d1 = n1.to_DFA()
    d1.minimize()

    d2 = DFA_SRC.DFA()
    d2.set_alphabet({'b'})
    d2.add_states(['q0','q1'])
    d2.set_q0('q0')
    d2.set_finish_states({'q1'})
    d2.set_deltas(
        {
            'q0':[('b','q1')]
        }
    )
    d3 = d1.intersection(d2)
    assert d3.run('a') == False
    assert d3.run('b') == True
    pass

def test_difference():
    n1 = NFA_SRC.NFA()
    n1.regex_to_NFA('(a|b)*')
    d1 = n1.to_DFA()
    d1.minimize()

    d2 = DFA_SRC.DFA()
    d2.set_alphabet({'a'})
    d2.add_states(['q0','q1'])
    d2.set_q0('q0')
    d2.set_finish_states({'q1'})
    d2.set_deltas(
        {
            'q0':[('a','q1')]
        }
    )

    d3 = DFA_SRC.DFA()
    d3.set_alphabet({'b'})
    d3.add_states(['q0','q1'])
    d3.set_q0('q0')
    d3.set_finish_states({'q1'})
    d3.set_deltas(
        {
            'q0':[('b','q1')]
        }
    )

    d4 = d1.difference(d2)
    assert d4.run('a') == False

    d5 = d4.difference(d3)
    assert d5.run('b') == False

    d6 = d5.difference(d1)
    assert d6.is_empty() == True

def test_all():
    test_dfa1()
    test_minimize()
    test_to_regex()
    test_is_equal1()
    test_is_equal2()
    test_is_equal3()

    test_complement1()
    test_complement2()

    test_union()

    test_intersection1()
    test_intersection2()

    test_difference()

if __name__ == '__main__':
    
    pass


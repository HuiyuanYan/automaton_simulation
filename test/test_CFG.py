import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.automata.CFG import CFG,LL_1_parser
def test_func():
    pass
def test_CFG1():
    variables = {'S'}
    terminals = {'a','b'}
    start_variable = 'S'
    g = CFG()
    g.set_variables(variables)
    g.set_terminals(terminals)
    g.set_start_variable(start_variable)
    g.add_production('S',['a','S','b'],test_func)
    g.add_production('S',[g.epsilon()],test_func)

    ll_1 = LL_1_parser(g)
    ll_1.construct_LL_1_analysis_table()
    assert ll_1.parse('aabb',True) == True
    assert ll_1.parse('ab',True) == True
    assert ll_1.parse('aab',True) == False


if __name__ == '__main__':
    test_CFG1()
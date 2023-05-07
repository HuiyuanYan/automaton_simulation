import os
import sys
import copy
from cmm_define import cmm_token_re_func
from lexer_shared_var import set_global_value,get_global_value
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from myToken.my_token import Token
from automata.DFA import DFA
from automata.NFA import NFA
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.dirname(__file__) + '\example.cmm'

input_str = ''

def read_src_file(file_name):
    global input_str
    with open(file_name) as f:
        set_global_value('line_no',1)
        input_str = f.read()
        set_global_value('input_str',input_str)
        print(input_str)

def generate_token_dfa():
    token_dfa_list = []
    for token,re,func in cmm_token_re_func:
        n = NFA()
        n.regex_to_NFA(re)
        token_dfa_list.append((token,copy.deepcopy(n)))
    return token_dfa_list

def dfa_recognize(begin,dfa:DFA):
    global input_str
    end_ptr = begin
    q = dfa.q0()
    deltas = dfa.deltas()
    alphabet = dfa.alphabet()
    finish = dfa.finish_states()
    last_matched = begin -1
    while end_ptr < len(input_str):
        ch = input_str[end_ptr]
        if q not in deltas or ch not in alphabet:
            break
        if_matched = False
        for c,p in deltas[q]:
            if ch == c:
                q = p
                end_ptr += 1
                if_matched = True
                break
        if q in finish:
            last_matched = end_ptr
        if if_matched == False:
            break
    if last_matched > begin:
        return(last_matched,True)
    else:
        return(begin,False)
    pass

def recognize_token():
    global input_str
    token_dfa_list = generate_token_dfa()
    token_list = []
    set_global_value('read_ptr',0)
    read_ptr = get_global_value('read_ptr')
    while read_ptr <len(input_str):
        if_matched = False
        for i in range(0,len(token_dfa_list)):
            token_name = token_dfa_list[i][0]
            dfa = token_dfa_list[i][1].to_DFA()
            new_read_ptr,result = dfa_recognize(read_ptr,dfa)
            if result == False:
                continue
            else:
                if_matched = True
                lexeme = input_str[read_ptr:new_read_ptr]
                token_list.append(Token(token_name,lexeme,get_global_value('line_no')))
                func = cmm_token_re_func[i][2]
                set_global_value('read_ptr',new_read_ptr)
                if func is not None:
                    func()
            
            read_ptr = get_global_value('read_ptr')

        if if_matched == False:
            print('Syntax Error!')
            exit(-1)
        pass
    print(token_list)
    pass

if __name__ == '__main__':
    read_src_file(file_path)
    recognize_token()
    print(get_global_value('line_no'))

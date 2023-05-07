# -*- coding: utf-8 -*-
global_dict = {
    'line_no':1,
    'input_str':'',
    'read_ptr':0
}

def get_lexer_input_ch():
    if global_dict['read_ptr'] < len(global_dict['input_str']):
        ch = global_dict['input_str'][global_dict['read_ptr']]
        global_dict['read_ptr'] += 1
        return ch
    else:
        return None

def set_global_value(key:str,value:any):
    global_dict[key] = value

def get_global_value(key):
    try:
        return global_dict[key]
    except:
        print(f'Global variable {key} does not exist.')


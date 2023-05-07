from lexer_shared_var import *

def func_endline():
    set_global_value('line_no',get_global_value('line_no')+1)

def func_single_line_comment():
    c = get_lexer_input_ch()
    while c != None and c != '\n':
        c = get_lexer_input_ch()
    pass

def func_multiline_comment():
    c = get_lexer_input_ch()
    state = 0;
    while True:
        if state == 0:
            if c == '*':
                state = 1
        
        elif state == 1:
            if c == '/':
                break
            else:
                state = 0
        c = get_lexer_input_ch()
    

cmm_token_re_func = [
        ("ENDLINE","\r\n|\n",func_endline),
        ("TAB","\t",None),
        ("BLANK"," ",None),
        ("SINGLE_LINE_COMMENT","//",func_single_line_comment),
        ("MULTILINE_COMMENT","/\*",func_multiline_comment),
        ("TYPE", "int|float",None),
        ("INT", "0|((1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*)",None),
        ("SEMI", ";",None),
        ("COMMA", ",",None),
        ("ASSIGNOP", "=",None),
        ("RELOP", ">|<|>=|<=|==|!=",None),
        ("PLUS", "\\+",None),
        ("MINUS", "\\-",None),
        ("STAR", "\\*",None),
        ("DIV", "\\/",None),
        ("AND", "\\&\\&",None),
        ("OR", "\\|\\|",None),
        ("DOT", "\\.",None),
        ("NOT", "\\!",None),
        ("LP", "\\(",None),
        ("RP", "\\)",None),
        ("LB", "\\[",None),
        ("RB", "\\]",None),
        ("LC", "\\{",None),
        ("RC", "\\}",None),
        ("STRUCT", "struct",None),
        ("RETURN", "return",None),
        ("IF", "if",None),
        ("ELSE", "else",None),
        ("WHILE", "while",None),
        ("ID","[a-zA-Z_]+[a-zA-Z0-9_]*",None)
]

if __name__ == '__main__':
    pass
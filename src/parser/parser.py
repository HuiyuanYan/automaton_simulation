import os
import sys
import copy
from typing import List
from parser_shared_var import attr_list
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from myToken.my_token import Token
from automata.CFG import CFG,LL_1_parser
class LL_1_parser_recognize_token(LL_1_parser):
    def __init__(self, input_CFG=None) -> None:
        super().__init__(input_CFG)
    def parse_token(self):
        print(super().__LL_1_analysis_table)
    pass

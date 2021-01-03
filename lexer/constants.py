""" regex patterns """
re_numeric_pattern = r'^[0-9]$'
re_charonly_pattern = r'^[a-zA-Z]&'
re_char_num_underlin_pattern = r'^\w$'

""" keywords and symbols """
S_EOF, S_Add, S_Sub, S_Mul, S_Div, S_Mod, S_Inc, S_Dec, \
S_Eql, S_Neq, S_Lss, S_Grt, S_Leq, S_Geq, S_Neq, \
S_And, S_Or, S_Not, \
S_Asgn, S_AddAsgn, S_SubAsgn, S_MulAsgn, S_DivAsgn, S_ModAsgn, \
S_True, S_False, S_null, \
S_Abstract, S_Continue, S_For, S_New, S_Switch, S_Default, S_If, S_Else, S_Private, S_This, S_Break, S_Public, \
S_Protected, S_Throw, S_Throws, S_Import, S_Enum, S_Return, S_Transient, S_Try, S_Catch, S_Extends, S_Final, \
S_Interface, S_Static, S_Void, S_Class, S_Finally, S_Super, S_While, \
S_Int, S_Double, S_Float, S_String, S_Boolean, S_Byte, S_Long, S_Short, S_Char, S_Dot, \
S_Lbrace, S_Rbrace, S_Lparen, S_Rparen, S_Semi, S_Comma, S_Identifier, S_LSquare_brac, S_RSquare_brac, S_question_mark, \
S_punctuation = range(78)

""" single character only symbols """
symbols = {'{': S_Lbrace, '}': S_Rbrace, '(': S_Lparen, ')': S_Rparen, ';': S_Semi, ',': S_Comma, '[': S_LSquare_brac,
           ']': S_RSquare_brac, '.': S_Dot, '?': S_question_mark, ':': S_punctuation}

""" keywords """
key_words = {'if': S_If, 'else': S_Else, 'while': S_While, 'true': S_True, 'false': S_False, 'null': S_null,
             'abstract': S_Abstract, 'continue': S_Continue, 'for': S_For, 'new': S_New, 'switch': S_Switch,
             'default': S_Default, 'if': S_If, 'else': S_Else, 'private': S_Private, 'this': S_This, 'break': S_Break,
             'public': S_Public, 'protected': S_Protected, 'throw': S_Throw, 'throws': S_Throws, 'import': S_Import,
             'enum': S_Enum, 'return': S_Return, 'transient': S_Transient, 'try': S_Try, 'catch': S_Catch,
             'extends': S_Extends, 'final': S_Final, 'interface': S_Interface, 'static': S_Static, 'void': S_Void,
             'class': S_Class, 'finally': S_Finally, 'super': S_Super, 'while': S_While, 'int': S_Int,
             'double': S_Double, 'float': S_Float, 'String': S_String, 'boolean': S_Boolean, 'byte': S_Byte,
             'long': S_Long, 'short': S_Short, 'char': S_Char}

""" symbol values """
symbol_values = ['end_of_file', 'op_add', 'op_sub', 'op_mul', 'op_div', 'op_mod', 'op_increment', 'op_decrement',
                 'op_equal',
                 'op_not_equal', 'op_less', 'op_grater', 'op_less_equal', 'op_grater_equal', 'op_not_equal', 'op_and',
                 'op_or', 'op_not', 'op_assign', 'op_add_asign', 'op_sub_assign', 'op_mul_assign', 'op_div_assign',
                 'op_mod_assign', 'keyword_true', 'keyword_false', 'keyword_null', 'keyword_abstract',
                 'keyword_continue', 'keyword_for', 'keyword_new', 'keyword_switch', 'keyword_default', 'keyword_if',
                 'keyword_else', 'keyword_private', 'keyword_this', 'keyword_break', 'keyword_public',
                 'keyword_protected', 'keyword_throw', 'keyword_thorws', 'keyword_import', 'keyword_enum',
                 'keyword_return', 'keyword_transient', 'keyword_try', 'keyword_catch', 'keyword_extends',
                 'keyword_final', 'keyword_interface', 'keyword_static', 'keyword_void', 'keyword_class',
                 'keyword_finally', 'keyword_super', 'keyword_while', 'keyword_int', 'keyword_double', 'keyword_float',
                 'keyword_string', 'keyword_boolean', 'keyword_byte', 'keyword_long', 'keyword_short', 'keyword_char',
                 'left_brace', 'right_brace', 'left_paren', 'right_paren', 'semicolon', 'comma', 'identifier',
                 'left_square_bracket', 'right_square_bracket', 'dot', 'question_mark', 'punctuation']

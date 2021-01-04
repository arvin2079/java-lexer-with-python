from . import constants

current_ch = " "
current_col = 0
current_line = 1
input_file = None


def print_error(line, col, msg):
    print(line, col, msg)
    exit(1)


def get_next_ch():
    global current_ch, current_col, current_line

    current_ch = input_file.read(1)
    current_col += 1
    if current_ch == '\n':
        current_line += 1
        current_col = 0
    return current_ch


def identity_or_num(err_line, err_col):
    content = ""
    is_floating_point = False

    if current_ch.isnumeric():
        content += current_ch
        while True:
            get_next_ch()
            if current_ch == '.':
                if not is_floating_point:
                    content += current_ch
                    get_next_ch()
                else:
                    print_error(err_line, err_col, 'error : wrong format number!')
                    exit(1)
                is_floating_point = True
            if current_ch.isnumeric():
                content += current_ch
            else:
                break

        if len(content) == 0:
            print_error(err_line, err_col, "format exeption in recognizing number!")
        if is_floating_point:
            return constants.S_Float, err_line, err_line, content
        else:
            return constants.S_Int, err_line, err_line, content

    elif current_ch.isidentifier():
        content += current_ch
        while True:
            get_next_ch()
            if current_ch.isalnum() or current_ch == '_':
                content += current_ch
            else:
                break

        if len(content) == 0:
            print_error(err_line, err_col, "format exeption in recognizing identifier!")
        if content in constants.key_words:
            return constants.key_words[content], err_line, err_col
        return constants.S_Identifier, err_line, err_col, content
    else:
        print_error(err_line, err_col, "format exeption!")
        exit(1)


## only for multiline comments
def div_or_comment(err_line, err_col):
    get_next_ch()
    if current_ch == '*':
        while True:
            get_next_ch()
            if not current_ch:
                print_error(err_line, err_col, 'reach end of the file and comment does not finished!')
            if current_ch == '*':
                if get_next_ch() == '/':
                    get_next_ch()
                    break
    else:
        get_next_ch()
        return constants.S_Div, err_line, err_col


def expect_string(err_line, err_col):
    text = ""
    while get_next_ch() != '"':
        if len(current_ch) == 0:
            print_error(err_line, err_col, "reach end of file while scanning string literal")
        text += current_ch

    get_next_ch()
    return constants.S_double_quote_string, err_line, err_col, text


def expect_char(err_line, err_col):
    char = get_next_ch()
    if get_next_ch() != "'":
        print_error(err_line, err_col, 'error : wrong format character')
        exit(1)
    get_next_ch()
    return constants.S_Character, err_line, err_col, char


def expect_follow(err_line, err_col, if_no_match_found, expects: map):
    get_next_ch()
    for expect in expects:
        if current_ch == expect:
            get_next_ch()
            return expects[expect], err_line, err_col

    if if_no_match_found == constants.S_EOF:
        print_error(err_line, err_col, "error: unrecognized character: (%d) '%c'" % (ord(current_ch), current_ch))

    return if_no_match_found, err_line, err_col


class Token:
    def __init__(self, tok_key, line, col):
        self.tok_key = tok_key
        self.line = line
        self.col = col

    def print(self, desc=None):
        value = f'{constants.symbol_values[self.tok_key]} - line: {self.line} - col: {self.col}'
        if desc:
            value += f' - {desc}'
        print(value)


def gettok():
    while current_ch.isspace():
        get_next_ch()

    err_line = current_line
    err_col = current_col

    if len(current_ch) == 0:
        return constants.S_EOF, err_line, err_col

    elif current_ch == '+':
        return expect_follow(err_line, err_col, constants.S_Add, {
            '=': constants.S_AddAsgn,
            '+': constants.S_Inc,
        })
    elif current_ch == '-':
        return expect_follow(err_line, err_col, constants.S_Sub, {
            '=': constants.S_SubAsgn,
            '-': constants.S_Dec,
        })
    elif current_ch == '*':
        return expect_follow(err_line, err_col, constants.S_Mul, {
            '=': constants.S_MulAsgn,
        })
    elif current_ch == '%':
        return expect_follow(err_line, err_col, constants.S_Mod, {
            '=': constants.S_ModAsgn,
        })
    elif current_ch == '=':
        return expect_follow(err_line, err_col, constants.S_Asgn, {
            '=': constants.S_Eql,
        })
    elif current_ch == '!':
        return expect_follow(err_line, err_col, constants.S_Not, {
            '=': constants.S_Neq,
        })
    elif current_ch == '<':
        return expect_follow(err_line, err_col, constants.S_Lss, {
            '=': constants.S_Leq,
        })
    elif current_ch == '>':
        return expect_follow(err_line, err_col, constants.S_Grt, {
            '=': constants.S_Geq,
        })
    elif current_ch == '&':
        return expect_follow(err_line, err_col, constants.S_And, {
            '&': constants.S_And,
        })
    elif current_ch == '|':
        return expect_follow(err_line, err_col, constants.S_Or, {
            '|': constants.S_Or,
        })
    elif current_ch == '/':
        return div_or_comment(err_line, err_col)
    elif current_ch == '"':
        return expect_string(err_line, err_col)
    elif current_ch == "'":
        return expect_char(err_line, err_col)
    elif current_ch in constants.symbols:
        sym = constants.symbols[current_ch]
        get_next_ch()
        return sym, err_line, err_col
    else:
        return identity_or_num(err_line, err_col)


def lex(input_file_address: str):
    global input_file

    with open(input_file_address, mode='r') as file:
        input_file = file
        while True:
            t = gettok()
            if t:
                token = Token(tok_key=t[0], line=t[1], col=t[2])
                if token.tok_key == constants.S_Int or\
                        token.tok_key == constants.S_Float or\
                        token.tok_key == constants.S_Identifier or\
                        token.tok_key == constants.S_String:
                    if len(t) == 4:
                        token.print(desc=t[3])
                    else:
                        token.print()
                else:
                    token.print()

                if token.tok_key == constants.S_EOF:
                    break


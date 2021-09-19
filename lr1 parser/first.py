from consts import *
from stdin_terminal_input import lines_list, none_terminal_list, terminal_list


def find_first_for_none_terminal(s):
    global lines_list, none_terminal_list, terminal_list

    if s in terminal_list:
        return set(s)

    for line in lines_list:
        head = line.split(arrow_sign)[0]
        tail = line.split(arrow_sign)[1]

        if tail == '':
            none_terminal_list[s].add_first(epsilone_char)
            continue

        if tail[0] == s:
            continue

        if head != s:
            continue

        counter = 0
        for non_t in tail:
            t = find_first_for_none_terminal(non_t)
            none_terminal_list[s].add_first(t - set(epsilone_char))
            if epsilone_char not in t:
                break

            if counter == len(tail) - 1:
                none_terminal_list[s].add_first(epsilone_char)
            counter = counter + 1

    return none_terminal_list[s].first


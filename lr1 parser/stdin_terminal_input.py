from re import *
from consts import *
from collections import OrderedDict
from ness_classes import Terminal, NonTerminal

terminal_list = OrderedDict()
none_terminal_list = OrderedDict()
lines_list = []


def stdin_input():
    global lines_list, terminal_list, none_terminal_list

    rep = 1
    while True:
        input_grammer = input()
        lines_list.append(input_grammer.replace(' ', ''))
        if lines_list[-1].lower() in ['', ]:
            del lines_list[-1]
            break

        head = lines_list[rep - 1].split(arrow_sign)[0]
        tail = lines_list[rep - 1].split(arrow_sign)[1]

        if head not in none_terminal_list.keys():
            none_terminal_list[head] = NonTerminal(head)

        terminal_list.update(find_with_reg(terminal_list, terminal_reg, tail))
        none_terminal_list.update(find_with_reg(none_terminal_list, none_terminal_reg, tail))

        rep += 1


def find_with_reg(goal_map,  reg, chosen_list):
    for i in finditer(reg, chosen_list):
        s = i.group()
        if s not in goal_map.keys():
            goal_map[s] = NonTerminal(s)
    return goal_map

# main()
# print(terminal_list.keys())
# print(none_terminal_list.keys())

from parser_main import parse
from stdin_terminal_input import lines_list
from consts import *


table = parse()


def alpha_number(w):
    num = 0
    for i in w:
        if (ord(i) >= 65 and ord(i) <= 90):
            num += 1
    return num


def draw_tree(actions, input_string):
    tree_length = 1
    tree_struct = []
    stack = []

    input_string = input_string.replace('$', '')
    input_string = list(reversed(input_string))

    for action in actions:
        action = list(action)[0]

        if action[0] == 's':
            input_char = input_string.pop()
            stack.append(input_char)
            tree_struct.append(list(input_char))
        elif action[0] == 'r':
            selected_grammar = lines_list[int(action[1])]
            grammar_head = selected_grammar.split(arrow_sign)[0]
            grammar_tail = selected_grammar.split(arrow_sign)[1]

            selected_tail = ''
            while selected_tail != grammar_tail:
                selected_tail = stack.pop() + selected_tail
            stack.append(grammar_head)

            index = len(stack) - 1
            if len(selected_tail) == 1:
                tree_struct[index].append(line_hori)
                tree_struct[index].append(grammar_head)
            elif len(selected_tail) == 2:
                tree_struct[index-1].append(line_hori * (tree_length - len(tree_struct[index-1])))
                tree_struct[index].append(line_hori * (tree_length - len(tree_struct[index])))
                tree_struct[index-1].append(line_horizontal_down)
                tree_struct[index].append(line_lower_right_corner)
                tree_struct[index-1].append(grammar_head)
            else:
                first_index = index - len(selected_tail) + 1
                tree_struct[first_index].append(line_hori * (tree_length - len(tree_struct[first_index])))
                tree_struct[index].append(line_hori * (tree_length - len(tree_struct[index])))
                tree_struct[first_index].append(line_horizontal_down)
                tree_struct[first_index].append(grammar_head)
                for iter_index in range(first_index + 1, index):
                    tree_struct[iter_index].append(line_hori * (tree_length - len(tree_struct[iter_index])))
                    tree_struct[iter_index].append(line_vertical_and_left)


            tree_length = len(max(tree_struct, key=len))

    for row in tree_struct:
        print(''.join(row))


test_input = "ccdd$"

input_stk = []
action_stk = []
cons_stk = []
stat_stk = []

stat_stk_len = 3 * len(test_input)
cons_stk_len = 5 * len(test_input)
input_stk_len = 5 * len(test_input)

for i in reversed(test_input):
    input_stk.append(i)

print(("%" + str(stat_stk_len) + "s") % "Stack", ("%" + str(cons_stk_len) + "s") % "Consumed", ("%" + str(input_stk_len) + "s") % "Input", "\t", "Action")

stat_stk.append(0)

try:
    while True:
        nextaction = table[stat_stk[-1]][input_stk[-1]]

        if (nextaction == "accept"):
            print("Accepted.")
            draw_tree(action_stk, test_input)
            break

        action_alpha = list(nextaction)[0][0]
        act = int(list(nextaction)[0][1])

        action_stk.append(nextaction)
        print(("%" + str(stat_stk_len) + "s") % stat_stk, ("%" + str(cons_stk_len) + "s") % cons_stk,  ("%" + str(input_stk_len) + "s") % input_stk, "\t", action_stk)

        if (action_alpha == "r"):
            reduction = lines_list[act]
            head = reduction.split(arrow_sign)[0]
            body = reduction.split(arrow_sign)[1]
            l = len(body)
            cnt = alpha_number(body)

            for i in range(l):
                cons_stk.pop()
                stat_stk.pop()

            cons_stk.append(head)
            nextstate = int(table[stat_stk[-1]][cons_stk[-1]])
            stat_stk.append(nextstate)

        elif (action_alpha == "s"):
            stat_stk.append(act)
            cons_stk.append(input_stk.pop())

except KeyError:
    print("Not Accepted!")

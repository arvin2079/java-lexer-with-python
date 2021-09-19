import first
from collections import OrderedDict
import stdin_terminal_input
from stdin_terminal_input import lines_list, none_terminal_list as none_t_list, terminal_list as t_list

from consts import *
from ness_classes import State, Item

none_terminal_list, terminal_list = [], []


def closure(items):
    def exists(new, items):

        for item in items:
            if item == new and sorted(set(item.look_forward)) == sorted(set(new.look_forward)):
                return True
        return False

    global lines_list

    while True:
        ctrl = 0
        for item in items:

            if item.index('.') == len(item) - 1:
                continue

            non_t = item.split(arrow_sign)[1].split('.')[1][0]

            if item.index('.') + 1 < len(item) - 1:
                lastr = list(first.find_first_for_none_terminal(item[item.index('.') + 2]) - set(chr(1013)))
            else:
                lastr = item.look_forward

            for line in lines_list:
                head = line.split(arrow_sign)[0]
                tail = line.split(arrow_sign)[1]

                if head != non_t:
                    continue

                new_i = Item(non_t + arrow_sign + '.' + tail, lastr)

                if not exists(new_i, items):
                    items.append(new_i)
                    ctrl = 1
        if ctrl == 0:
            break
    return items


def goto(items, s):
    init = []
    global lines_list

    for item in items:
        if item.index('.') == len(item) - 1:
            continue

        head = item.split(arrow_sign)[0]
        tail = item.split(arrow_sign)[1]

        revealed = tail.split('.')[0]
        not_revealed = tail.split('.')[1]

        if not_revealed[0] == s and len(not_revealed) >= 1:
            init.append(
                Item(head + arrow_sign + revealed + not_revealed[0] + '.' + not_revealed[1:], item.look_forward))

    return closure(init)


def enumerate_states():
    def contains(states, t):
        for state in states:
            if len(state) != len(t):
                continue
            if sorted(state) == sorted(t):
                for i in range(len(state)):
                    if state[i].look_forward != t[i].look_forward: break
                else:
                    return True
        return False

    global lines_list, none_terminal_list, terminal_list

    head = lines_list[0].split(arrow_sign)[0]
    tail = lines_list[0].split(arrow_sign)[1]

    states = [closure([Item(head + arrow_sign + '.' + tail, ['$'])])]

    while True:
        ctrl = 0
        for state in states:
            for k in none_terminal_list + terminal_list:
                t = goto(state, k)
                if t == [] or contains(states, t):
                    continue

                states.append(t)
                ctrl = 1
        if not ctrl:
            break
    return states


def augment_grammar():
    for i in range(ord('Z'), ord('A') - 1, -1):
        if chr(i) not in none_terminal_list:
            start_prod = lines_list[0]
            lines_list.insert(0, chr(i) + arrow_sign + start_prod.split(arrow_sign)[0])
            return


def create_tables(states):
    global none_terminal_list, terminal_list

    def stateNo(t):
        for state in states:
            if len(state.closure) != len(t):
                continue
            if sorted(state.closure) == sorted(t):
                for i in range(len(state.closure)):
                    if state.closure[i].look_forward != t[i].look_forward:
                        break
                else:
                    return state.no
        return -1

    def linesNo(closure):
        closure = ''.join(closure).replace('.', '')
        return lines_list.index(closure)

    SLR_tab = OrderedDict()
    for i in range(len(states)):
        states[i] = State(states[i])

    for s in states:
        SLR_tab[s.no] = OrderedDict()
        for item in s.closure:
            head = item.split(arrow_sign)[0]
            tail = item.split(arrow_sign)[1]
            nxtsy = tail.split('.')[1]
            if nxtsy == '':
                if linesNo(item) == 0:
                    SLR_tab[s.no]['$'] = 'accept'
                else:
                    for lfi in item.look_forward:
                        if lfi not in SLR_tab[s.no].keys():
                            SLR_tab[s.no][lfi] = {'r' + str(linesNo(item))}
                        else:
                            SLR_tab[s.no][lfi] |= {'r' + str(linesNo(item))}
                continue
            nxtsy = nxtsy[0]

            t = goto(s.closure, nxtsy)

            if t:
                if nxtsy in terminal_list:
                    if nxtsy not in SLR_tab[s.no].keys():
                        SLR_tab[s.no][nxtsy] = {'s' + str(stateNo(t))}
                    else:
                        SLR_tab[s.no][nxtsy] |= {'s' + str(stateNo(t))}
                else:
                    SLR_tab[s.no][nxtsy] = str(stateNo(t))
    return SLR_tab


def parse():
    global lines_list, none_t_list, none_terminal_list, t_list, terminal_list

    stdin_terminal_input.stdin_input()

    sep = "*" * 20
    print(sep + "non terminals first" + sep)
    for nt in none_t_list:
        first.find_first_for_none_terminal(nt)
        print(f"first set for < {nt} >: ", first.find_first_for_none_terminal(nt))

    augment_grammar()
    none_terminal_list = list(none_t_list.keys())
    terminal_list = list(t_list.keys()) + ['$']
    enm_st = enumerate_states()

    ctr = 0
    print("\n\n" + sep + " machine item states " + sep)
    for st in enm_st:
        print(f"\n\nitem number {ctr}:" if ctr != 0 else f"item number {ctr}")
        print("=" * 28)
        for i in st:
            string = "|" + "{:^25}".format(str(i)) + " |"
            line = "+" + ("-" * (len(string) - 2)) + "+"
            print(string)
            print(line)
        ctr += 1

    table = create_tables(enm_st)

    print("\n\n" + sep + " parse TABLE " + sep)

    sr, rr = 0, 0

    for i, enm_st in table.items():
        print(i, "\t", enm_st.items())
        st, r = 0, 0

        for p in enm_st.values():
            if p != 'accept' and len(p) > 1:
                p = list(p)
                if ('r' in p[0]):
                    r += 1
                else:
                    st += 1
                if ('r' in p[1]):
                    r += 1
                else:
                    st += 1
        if r > 0 and st > 0:
            sr += 1
        elif r > 0:
            rr += 1
    print('-' * 60)
    return table


if __name__ == "__main__":
    table = parse()

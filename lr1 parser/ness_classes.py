class Terminal:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class NonTerminal:

    def __init__(self, s):
        self.s = s
        self.first = set()

    def __str__(self):
        return self.s + " first: " + self.first

    def add_first(self, s): self.first.update(s)


class State:
    _state_id = 0

    def __init__(self, closure):
        self.closure = closure
        self.no = State._state_id
        State._state_id += 1


class Item(str):
    def __new__(cls, item, look_forward=list()):
        self = str.__new__(cls, item)
        self.look_forward = look_forward
        return self

    def __str__(self):
        return super(Item, self).__str__() + ", " + '|'.join(self.look_forward)

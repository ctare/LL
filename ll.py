#!/usr/bin/python3
import re

## tmp ################
import ply_util as pu
pu.def_tokens(
    PLUS=r"\+",
    ID=r"[a-zA-Z]+"
    )

lx = pu.lex()
lx.input("a + bcd + okok")
#######################
is_terminal = re.compile("[A-Z]+")

class TokenList(list):
    @staticmethod
    def parse(code):
        pass


class Fset:
    def __init__(self):
        self.defines = []

    def add(self, rule):
        if self != rule: self.defines.append(rule)


class First(Fset): pass


class Follow(Fset): pass


class Director:
    pass


class Terminal:
    def __init__(self, name):
        self.name = name

    def first(self):
        return self

    def __str__(self):
        return self.name


class Nonterminal:
    pass


class Grammer:
    def __init__(self, *rule):
        self.rules = [list(rule)]
        self.sub = None
        self.defined = False
        self.is_sub = False

    def first(self):
        return self.firsts

    def follow(self):
        return self.follows

    def add_first(self, rule):
        self.firsts.add(rule[0].first())

    def add_follow(self, rule):
        length = len(rule)
        for i, r in enumerate(rule):
            if not isinstance(r, Terminal) and not r.is_sub:
                if i + 1 < length:
                    target = rule[i + 1]
                    r.follows.add(target.first())
                    if not isinstance(target, Terminal) and EMPTY in target.first().defines:
                        r.follows.add(target.follow())
                else:
                    target = self
                    if r != target:
                        r.follows.add(target.follow())
                        # try:
                        #     print(target, r.follow().defines[0].defines)
                        # except: pass
                # print()
                # print(i, r, rule[i + 1] if i + 1 < length else self)

    def __or__(self, rule):
        for r in rule.rules:
            if self == r[0]:
                # 左再帰の除去
                if not self.sub:
                    self.sub = Grammer(EMPTY).define()
                    self.sub.follows = self.follow()
                    self.sub.is_sub = True
                    for sr in self.rules:
                        sr.append(self.sub)
                self.sub |= Grammer(*(r[1:] + [self.sub]))
            else:
                self.rules.append(r)
                if self.defined:
                    self.add_first(r)
                    self.add_follow(r)
        # self.firsts.add(rule.firsts)
        # self.follows.add(rule.follows)

        # self.rules += rule.rules
        # self.firsts += rule.firsts
        # self.follows += self.follows
        return self

    def start(self):
        self.follows.add(EOL)
        return self

    def define(self):
        self.firsts = First()
        self.follows = Follow()
        self.add_first(self.rules[0])
        self.add_follow(self.rules[0])
        self.defined = True
        return self




    # def __str__(self):
    #     return "<" + (" | ".join(["[" + (", ".join(map(lambda x: "__self__" if x == self else str(x), rule))) + "]" for rule in self.rules])) + ">"
def terminals(fset):
    result = []
    for rule in fset.defines:
        # ################
        # if fset == e.follow():
        #     print("r", rule)
        # if rule == e.sub.follow():
        #     print("ok")
        # ################
        if isinstance(rule, Fset):
            result += terminals(rule)
        else:
            result.append(rule)
    if isinstance(fset, First):
        return result
    else:
        result = set(result)
        if EMPTY in result: result.remove(EMPTY)
        return result


EOL = Terminal("EOL")
EMPTY = Terminal("EMPTY")
ID = Terminal("ID")
PLUS = Terminal("PLUS")
MINUS = Terminal("MINUS")
# expression = Grammer(ID)
# expression |= Grammer(expression, PLUS, ID) 
# expression |= Grammer(expression, MINUS, ID)

DIV = Terminal("DIV")
TIM = Terminal("TIM")
RP = Terminal("RP")
LP = Terminal("LP")
f = Grammer(ID).define()
t = Grammer(f).define()
e = Grammer(t).define().start()

f |= Grammer(LP, e, RP)
t |= Grammer(t, TIM, f)
e |= Grammer(e, PLUS, t)
# print(e.sub.follow().defines[0].defines)
#
# print("- - -")
# print(f)
# print(t, t.sub)
# print(e, e.sub)
#
# print("- - -")
# print(*map(str, terminals(e.first())))
# print(e.follow().defines)
# print(*map(str, terminals(e.follow())))
# print(*map(str, terminals(e.sub.firsts)))
# print(*map(str, terminals(t.firsts)))
# print(*map(str, terminals(t.sub.firsts)))
# print(*map(str, terminals(f.firsts)))

# print(expression.first())
"""
expr : expr PLUS value
     | value

     |
     v
expr | value expr2

expr2 : PLUS value expr2
      | EMPTY
"""
# grammer.add("expr : expr PLUS value")
# grammer.add("expr : value")
# grammer.add("value : ID")
# grammer.add("expr : ID PLUS")

# grammer.start("s")
# grammer.director()

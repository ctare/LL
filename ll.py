#!/usr/bin/python3
import re

## tmp ################
import ply_util as pu
pu.def_tokens(
    PLUS=r"\+",
    TIM=r"\*",
    LP=r"\(",
    RP=r"\)",
    ID=r"[a-zA-Z]+"
    )

lx = pu.lex()
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
        if self != rule:
            self.defines.append(rule)


class First(Fset):
    pass


class Follow(Fset):
    pass


class Director:
    def __init__(self):
        self.rule_map = {}

    def add(self, define, rule):
        if define not in self.rule_map:
            self.rule_map[define] = {}
        self.rule_map[define][rule[0].first()] = rule

    def get(self, grammer):
        return self.rule_map[grammer]


class Language:
    def __init__(self):
        self.directors = Director()
        self.start = None

    def director(self):
        rules = {}
        for grammer, firsts in self.directors.rule_map.items():
            rules[grammer] = {}
            for first, rule in firsts.items():
                for fi in terminals(first):
                    if fi == EMPTY:
                        for follow in terminals(grammer.follow()):
                            rules[grammer][follow] = [EMPTY]
                    else:
                        rules[grammer][fi] = rule
        return rules

    def add_director(self, grammer, rule):
        self.directors.add(grammer, rule)

    def execute(self, code):
        lx.input(code)
        code = []
        while True:
            t = lx.token()
            if not t:
                break
            code.append(globals()[t.type])
        trace(self.start, code, self.director())


def trace(start, inp, director):
    stack = [EOL, start]
    inp.append(EOL)
    while True:
        if not (inp or stack): break
        rule, terminal = stack[-1], inp[0]
        del stack[-1]
        if rule == terminal:
            del inp[0]
            continue
        # elif rule == EMPTY:
        next_rule = director[rule][terminal]
        if next_rule == [EMPTY]:
            continue
        else:
            print(sss([rule]), sss(next_rule))
            for x in next_rule[::-1]:
                stack.append(x)


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
        self.language.add_director(self, rule)

    def add_follow(self, rule):
        length = len(rule)
        for i, r in enumerate(rule):
            if not isinstance(r, Terminal) and not r.is_sub:
                if i + 1 < length:
                    target = rule[i + 1]
                    r.follows.add(target.first())
                    if not isinstance(
                            target, Terminal
                            ) and EMPTY in target.first().defines:
                        r.follows.add(target.follow())
                else:
                    target = self
                    if r != target:
                        r.follows.add(target.follow())

    def __or__(self, rule):
        for r in rule.rules:
            if self == r[0]:
                # 左再帰の除去
                if not self.sub:
                    self.sub = Grammer(EMPTY).define(self.language)
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
        return self

    def start(self):
        self.follows.add(EOL)
        self.language.start = self
        return self

    def define(self, language):
        if len(self.rules) != 1:
            print("warn: definition is multiple.")
        self.language = language
        self.firsts = First()
        self.follows = Follow()
        self.add_first(self.rules[0])
        self.add_follow(self.rules[0])
        self.defined = True
        return self


def terminals(fset):
    if isinstance(fset, Terminal):
        return [fset]
    result = []
    for rule in fset.defines:
        if isinstance(rule, Fset):
            result += terminals(rule)
        else:
            result.append(rule)
    if isinstance(fset, First):
        return result
    else:
        result = set(result)
        if EMPTY in result:
            result.remove(EMPTY)
        return result

test_lang = Language()

EOL = Terminal("EOL")
EMPTY = Terminal("EMPTY")
ID = Terminal("ID")
PLUS = Terminal("PLUS")
MINUS = Terminal("MINUS")

DIV = Terminal("DIV")
TIM = Terminal("TIM")
RP = Terminal("RP")
LP = Terminal("LP")
f = Grammer(ID).define(test_lang)
t = Grammer(f).define(test_lang)
e = Grammer(t).define(test_lang).start()

f |= Grammer(LP, e, RP)
t |= Grammer(t, TIM, f)
e |= Grammer(e, PLUS, t)

to_s = {e: "e", e.sub: "e_sub", t: "t", t.sub: "t_sub", f: "f"}
def sss(xx):
    return [ss(x) for x in xx]
def ss(t_or_g):
    if isinstance(t_or_g, Terminal):
        return t_or_g.name
    else:
        return to_s[t_or_g]

test_lang.execute("""
        a + b * c
""")

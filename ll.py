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

class Tokens:
    @staticmethod
    def parse(code):
        pass


class First:
    def __init__(self):
        self.defines = set()

    def add(self, first_rule):
        if self != first_rule: self.defines.add(first_rule)


class Follow:
    def __init__(self):
        self.defines = set()

    def add(self, follow_rule):
        if self != follow_rule: self.defines.add(follow_rule)


class Director:
    pass


class Nonterminal:
    pass


class Grammer:
    def __init__(self):
        self.firsts = {}
        self.follows = {}

    def get_first(self, define):
        if define not in self.firsts:
            self.firsts[define] = First()
        return self.firsts[define]

    def first(self, define, first_rule):
        f = self.get_first(define)

        if is_terminal.match(first_rule):
            # is terminal
            f.add(first_rule)
        else:
            # is nonterminal
            f.add(self.get_first(first_rule))

    def get_follow(self, target_rule):
        if target_rule not in self.follows:
            self.follows[target_rule] = Follow()
        return self.follows[target_rule]

    def follow(self, target_rule, follow_rule):
        if is_terminal.match(target_rule):
            return None

        f = self.get_follow(target_rule)

        if is_terminal.match(follow_rule):
            # is terminal
            f.add(follow_rule)
        else:
            # is nonterminal
            f.add(self.get_follow(follow_rule))

    def add(self, expression):
        define, rule = list(map(lambda x: x.strip(), expression.split(":")))
        rule = rule.split()
        self.first(define, rule[0])
        for i, r in enumerate(rule):
            if i == len(rule) - 1:
                self.follow(r, define)
            else: self.follow(r, rule[i + 1])

    def start(self, define):
        self.get_follow(define).add("EOL")

    @staticmethod
    def create_table(grammer):
        """
        Director(firsts, follows)
        """
        pass


grammer = Grammer()
grammer.add("expr : expr PLUS value")
grammer.add("expr : value")
grammer.add("value : ID")
grammer.start("expr")
"""

table = Grammer.create_table(grammer)
    
"""

import re


class Tokens:
    @staticmethod
    def parse(code):
        pass


class First:
    pass


class Follow:
    pass


class Director:
    pass


class Nonterminal:
    pass


class Grammer:
    """
    firsts, follows
    """
    def add(expression):
        """
        -- expr : value PLUS value --
        define: expr
        rule: [value, PLUS, value]

        First(grammer, expr)
        for r in rule: Follow(grammer, r)
        """
        pass

    @staticmethod
    def create_table(grammer):
        """
        Director(firsts, follows)
        """
        pass



"""

grammer = Grammer()
grammer.add("expr : value PLUS value", fnc1)
grammer.add("expr : value", fnc2)
grammer.add("value : ID", fnc3)

table = Grammer.create_table(grammer)
    
"""
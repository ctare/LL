#!/usr/bin/python3
import re

class TokenDefines(dict):
    def __init__(self, defines):
        for k, v in defines.items():
            defines[k] = re.compile(v)
        super().__init__(defines)
        self.ignore_def = re.compile("")

    def parse(self, code):
        result = []
        before = code
        while code:
            for k, v in sorted(self.items(), key=lambda x: len(x[1].pattern), reverse=True):
                m = self.ignore_def.match(code)
                if m:
                    code = code[m.end():]
                m = v.match(code)
                if m:
                    result.append(Token(k, m.group()))
                    code = code[m.end():]
            if before == code:
                raise ParseError(before)
            before = code
        return result

    def ignore(self, ignore_def):
        self.ignore_def = re.compile(ignore_def)
        return self


class Token:
    def __init__(self, terminal, value):
        self.terminal = terminal
        self.value = value


class ParseError(Exception):
    def __init__(self, key):
        super().__init__("no match '{}'".format(key))

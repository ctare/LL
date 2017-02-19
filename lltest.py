#!/usr/bin/python3
from ll import *

print("\n - test - ")
errors = []
def test(message, **args):
    def decorator(f):
        print("test:", message)
        try:
            f(**args)
        except Exception as e:
            print("error\n")
            errors.append((f, message))
    return decorator


def first_match(origin_list, grammer):
    origin_list = list(origin_list)
    target_list = list(terminals(grammer.first()))
    no_such = []
    for t in target_list:
        if t in origin_list:
            origin_list.remove(t)
        else: no_such.append(t)
    return not origin_list, [x.name for x in origin_list], [x.name for x in no_such]


def follow_match(origin_list, grammer):
    origin_list = list(origin_list)
    target_list = set(terminals(grammer.follow()))
    no_such = []
    for t in target_list:
        if t in origin_list:
            origin_list.remove(t)
        else: no_such.append(t)
    return not (origin_list or no_such), [x.name for x in origin_list], [x.name for x in no_such]



def calc_director(grammer):
    director = grammer.language.director
    firsts = director.get(grammer)
    rules = {}
    for first, rule in firsts.items():
        for fi in terminals(first):
            if fi == EMPTY:
                for follow in terminals(grammer.follow()):
                    rules[follow] = [EMPTY]
            else:
                rules[fi] = rule
    return rules

def director_match(origin_list, grammer):
    origin_list = list(origin_list)
    target_dict = calc_director(grammer)
    origin_dict = dict(zip(tlist, origin_list))
    not_enough = []
    too_many = []
    for k, v in origin_dict.items():
        try:
            if target_dict[k] != v:
                not_enough.append(target_dict[k])
        except KeyError:
            if v != n:
                too_many.append(v)
    return not (not_enough or too_many), not_enough, too_many


def p(*inspect):
    print("test message:", inspect)
# ID = Terminal("ID")
# PLUS = Terminal("PLUS")
# DIV = Terminal("DIV")
# TIM = Terminal("TIM")
# RP = Terminal("RP")
# LP = Terminal("LP")
# f = Grammer(ID).define().start()
# t = Grammer(f).define()
# e = Grammer(t).define()

print("""
        e : e + t | t
        t : t * f | f
        f : (e)   | ID
""")

@test("e grammer")
def F():
    assert e.rules[0] == [t, e.sub]

@test("e sub grammer")
def F():
    assert e.sub.rules == [[EMPTY], [PLUS, t, e.sub]]

@test("t grammer")
def F():
    assert t.rules[0] == [f, t.sub]

@test("t sub grammer")
def F():
    assert t.sub.rules == [[EMPTY], [TIM, f, t.sub]]

@test("f grammer")
def F():
    assert f.rules == [[ID], [LP, e, RP]]


@test("e first")
def F():
    match, at, dif = first_match([LP, ID], e)
    if at or dif: print(at, dif)
    assert match

@test("e sub first")
def F():
    match, at, dif = first_match([PLUS, EMPTY], e.sub)
    if at or dif: print(at, dif)
    assert match

@test("t first")
def F():
    match, at, dif = first_match([LP, ID], t)
    if at or dif: print(at, dif)
    assert match

@test("t sub first")
def F():
    match, at, dif = first_match([TIM, EMPTY], t.sub)
    if at or dif: print(at, dif)
    assert match

@test("f first")
def F():
    match, at, dif = first_match([LP, ID], f)
    if at or dif: print(at, dif)
    assert match

@test("e follow")
def F():
    match, at, dif = follow_match([RP, EOL], e)
    if at or dif: print(at, dif)
    assert match

@test("e sub follow")
def F():
    match, at, dif = follow_match([RP, EOL], e.sub)
    if at or dif: print(at, dif)
    assert match

@test("t follow")
def F():
    match, at, dif = follow_match([PLUS, RP, EOL], t)
    if at or dif: print(at, dif)
    assert match

@test("t sub follow")
def F():
    match, at, dif = follow_match([PLUS, RP, EOL], t.sub)
    if at or dif: print(at, dif)
    assert match

@test("f follow")
def F():
    match, at, dif = follow_match([PLUS, TIM, RP, EOL], f)
    if at or dif: print(at, dif)
    assert match

n = None
tlist = [ID, PLUS, TIM, LP, RP, EOL]
@test("e director")
def F():
    match, not_enough, too_many = director_match([
        [t, e.sub], n, n, [t, e.sub], n, n
        ], e)
    if not_enough or too_many:
        print(not_enough)
        print(too_many)
    assert match

@test("e sub director")
def F():
    match, not_enough, too_many = director_match([
        n, [PLUS, t, e.sub], n, n, [EMPTY], [EMPTY]
        ], e.sub)
    if not_enough or too_many:
        print(not_enough)
        print(too_many)
    assert match

@test("t director")
def F():
    match, not_enough, too_many = director_match([
        [f, t.sub], n, n, [f, t.sub], n, n
        ], t)
    if not_enough or too_many:
        print(not_enough)
        print(too_many)
    assert match

@test("t sub director")
def F():
    match, not_enough, too_many = director_match([
        n, [EMPTY], [TIM, f, t.sub], n, [EMPTY], [EMPTY]
        ], t.sub)
    if not_enough or too_many:
        print(not_enough)
        print(too_many)
    assert match

@test("f director")
def F():
    match, not_enough, too_many = director_match([
        [ID], n, n, [LP, e, RP], n, n
        ], f)
    if not_enough or too_many:
        print(not_enough)
        print(too_many)
    assert match


print("\n - errors %d -\n%s" %(len(errors), "\n".join(map(lambda x: x[1], errors))))
for f, m in errors:
    f()

from math import floor
from functools import reduce


def get_input():
    rules: list[tuple[int, int]] = list()
    updates: list[tuple[int, ...]] = list()
    target = rules
    sep = "|"
    with open("input.txt", "r") as f:
        for l in f:
            l = l.strip()
            if l == "":
                target = updates
                sep = ","
                continue
            target.append(tuple(map(int, l.split(sep))))
    return rules, updates


def get_update_rules(update, rules):
    relevant_rules = list()
    for p in update:
        relevant_rules.extend((r for r in rules if p in r and r not in relevant_rules))
    return relevant_rules


def get_must_precede_list(page, upd_rules):
    x = tuple((r[1] for r in upd_rules if r[0] == page))
    # print(f"Page {page} must precede:", x)
    return x


def validate_update(update, rules):
    # print(f"Checking update {update}")
    upd_rules = get_update_rules(update, rules)
    for idx, page in enumerate(update):
        must_precede = get_must_precede_list(page, upd_rules)
        preceding_pages: tuple = update[:idx]
        for mp_pg in must_precede:
            if mp_pg in preceding_pages:
                return False
    return True


def middle(upd):
    return upd[floor(len(upd) / 2)]


all_rules, all_updates = get_input()
res = reduce(lambda acc, u: acc + (middle(u) if validate_update(u, all_rules) else 0), all_updates, 0)
print(res)

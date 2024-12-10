from math import floor
from functools import reduce, cmp_to_key


def get_input():
    rules: list[tuple[int, int]] = list()
    updates: list[list[int]] = list()
    target = rules
    sep = "|"
    with open("input.txt", "r") as f:
        for l in f:
            l = l.strip()
            if l == "":
                target = updates
                sep = ","
                continue
            target.append(list(map(int, l.split(sep))))
    return rules, updates


def get_update_rules(update, rules):
    relevant_rules = list()
    for p in update:
        relevant_rules.extend((r for r in rules if p in r and r not in relevant_rules))
    return relevant_rules


def get_bidir_pages(page, upd_rules):
    fol = [r[1] for r in upd_rules if r[0] == page]
    prec = [r[0] for r in upd_rules if r[1] == page]
    return prec, fol


def validate_update(update, upd_rules):
    for idx, page in enumerate(update):
        _, fol = get_bidir_pages(page, upd_rules)
        preceding_pages = update[:idx]
        for mp_pg in fol:
            if mp_pg in preceding_pages:
                return False
    return True


def cmp(upd_rules):
    def _cmp(a,b):
        prec, fol = get_bidir_pages(a, upd_rules)
        if b in prec:
            return 1
        if b in fol:
            return -1
        return 0
    return _cmp


def middle(upd):
    return upd[floor(len(upd) / 2)]


all_rules, all_updates = get_input()

bad_updates = list(filter(lambda u: not validate_update(u, all_rules), all_updates))
cmp_all = cmp(all_rules)
for upd in bad_updates:
    upd.sort(key=cmp_to_key(cmp_all))
res = reduce(lambda acc, u: acc + middle(u), bad_updates, 0)
print(res)

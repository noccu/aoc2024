from math import floor
from functools import reduce


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


def get_must_precede_list(page, upd_rules):
    x = tuple((r[1] for r in upd_rules if r[0] == page))
    # print(f"Page {page} must precede:", x)
    return x


def validate_update(update, upd_rules):
    # print(f"Checking update {update}")
    for idx, page in enumerate(update):
        must_precede = get_must_precede_list(page, upd_rules)
        preceding_pages: tuple = update[:idx]
        for mp_pg in must_precede:
            if mp_pg in preceding_pages:
                return False, (idx, mp_pg)
    return True, (None, None)


def fix_update_still_dumb(upd, rules):
    upd_rules = get_update_rules(upd, rules)
    sort_map = {p: i for i, p in enumerate(upd)}
    for pg, i in sort_map.items():
        for following_page in get_must_precede_list(pg, upd_rules):
            if following_page not in sort_map:
                continue
            if sort_map[following_page] > sort_map[pg]:
                continue
            sort_map[following_page] = sort_map[pg] + i
    presorted_upd = list(sort_map.keys())
    presorted_upd.sort(key=lambda x: sort_map[x])
    if not validate_update(presorted_upd, upd_rules)[0]:
        return fix_update_still_dumb(presorted_upd, rules)
    return presorted_upd


def middle(upd):
    return upd[floor(len(upd) / 2)]


all_rules, all_updates = get_input()
bad_updates = filter(lambda u: not validate_update(u, all_rules)[0], all_updates)
res = reduce(
    lambda acc, u: acc + middle(u), map(lambda u: fix_update_still_dumb(u, all_rules), bad_updates), 0
)
print(res)

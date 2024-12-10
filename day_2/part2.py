from itertools import pairwise, permutations
import sys

PROBLEM_DAMPENER = int(sys.argv[1]) if len(sys.argv) > 1 else 0
print(f"Problem dampener: {PROBLEM_DAMPENER}")


def get_reports():
    with open("input.txt", "r") as f:
        return map(lambda r: map(int, r.split()), f.readlines())


# def find_trend_problems(level_diffs):
#     inc = list(filter(lambda x: x > 0, level_diffs))
#     dec = list(filter(lambda x: x < 0, level_diffs))
#     diff = sorted((inc, dec), key=len)
#     return diff[0]


# def find_value_problems(level_diffs):
#     return list(filter(lambda d: not (0 < abs(d) < 4), level_diffs))


def is_safe(r):
    prev_last_lvl: int = None
    for last_lvl, lvl in pairwise(r):
        if not (0 < abs(last_lvl - lvl) < 4) or (
            prev_last_lvl is not None
            and not (prev_last_lvl < last_lvl < lvl or prev_last_lvl > last_lvl > lvl)
        ):
            return False
        prev_last_lvl = last_lvl
    return True


def report_perms(r: list):
    yield r
    for p in range(1, PROBLEM_DAMPENER + 1):
        try_without = permutations(range(0, len(r)), p)
        for n in try_without:
            yield (x for i, x in enumerate(r) if i not in n)


def validate_reports(report):
    report = list(report)
    return any(map(is_safe, report_perms(report)))


# Yay, interpreter opts!
print(len(list(filter(validate_reports, get_reports()))))

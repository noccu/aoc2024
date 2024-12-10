from itertools import pairwise


def get_reports():
    with open("input.txt", "r") as f:
        return map(lambda r: map(int, r.split()), f.readlines())


def is_safe(report):
    level_diffs = list(map(lambda x: x[0] - x[1], pairwise(report)))
    abs_diffs = map(abs, level_diffs)
    abs_sum = 0
    for d in abs_diffs:
        if not (0 < d < 4):
            return False
        abs_sum += d
    diff_sum = sum(level_diffs)
    if abs_sum != abs(diff_sum):
        return False
    return True

# Yay, interpreter opts!
print(len(list(filter(is_safe, get_reports()))))

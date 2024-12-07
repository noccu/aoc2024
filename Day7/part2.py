from operator import add, mul
from itertools import product


def cat(a, b):
    return int(str(a) + str(b))


def get_input():
    out = list()
    with open("input.txt", "r") as f:
        for l in f:
            res, nums = l.split(": ")
            nums = map(int, nums.strip().split(" "))
            out.append((int(res), tuple(nums)))
        return out


def genFormulae(n):
    op_perms = product(ALLOWED_OPS, repeat=len(n) - 1)
    for perm in op_perms:
        yield zip((add, *perm), n)


def calc(n: tuple[int, ...]):
    for f in genFormulae(n):
        r = 0
        for op, num in f:
            r = op(r, num)
        yield r


ALLOWED_OPS = (add, mul, cat)
res = 0
for target, nums in get_input():
    for c in calc(nums):
        if c == target:
            res += c
            break
print(res)

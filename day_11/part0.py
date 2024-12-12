from time import process_time
from math import floor


def get_input():
    with open("input.txt") as f:
        return f.readline().strip().split(" ")


LOOKUP = dict()


def get_stones(num, iterations):
    if iterations == 0:
        return 1

    m = LOOKUP.get(num)
    if not m:
        LOOKUP[num] = m = dict()
    i = m.get(iterations)
    if not i:
        m[iterations] = i = calc(num, iterations)
    return i


def calc(num, iterations):
    new_nums = blink(num)
    new_stones = 0
    LOOKUP[num][1] = new_stones  # small efficiency boost?
    for n in new_nums:
        sub_stones = get_stones(n, iterations - 1)
        new_stones += sub_stones
    return new_stones if new_stones > 0 else len(new_nums)


def blink(num: str):
    if num == "0":
        num = "1"
    elif len(num) & 1 == 0:
        half_idx = floor(len(num) / 2)
        left_split = str(int(num[:half_idx]))
        right_split = str(int(num[half_idx:]))
        return (left_split, right_split)
    else:
        num = str(2024 * int(num))
    return (num,)


start = process_time()
res_1 = 0
res_2 = 0
for i, num in enumerate(get_input()):
    n_res_1 = get_stones(num, 25)
    n_res_2 = get_stones(num, 75)
    res_1 += n_res_1
    res_2 += n_res_2
    print(f"Number {i}: {num}: {n_res_1}, {n_res_2}")
end = process_time()
print(f"Part 1: {res_1}")
print(f"Part 2: {res_2}")
print(f"Took: {end-start}s")

import re

def get__input():
    with open("input.txt", "r") as f:
        return "".join(f.readlines())

res = 0
for x,y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", get__input()):
    res += int(x) * int(y)

print(res)

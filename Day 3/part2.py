import re

def get__input():
    with open("input.txt", "r") as f:
        return "".join(l.strip() for l in f.readlines())

cleaned = re.sub(r"don't\(\).+?(?:do\(\)|$)", "", get__input())
res = 0
for x,y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", cleaned):
    res += int(x) * int(y)

print(res)

from functools import reduce

listA = list()
listB = list()

with open("input.txt", "r") as f:
    for l, r in map(lambda x: x.split(), f.readlines()):
        listA.append(int(l))
        listB.append(int(r))

listA.sort()
listB.sort()
res = reduce(lambda o, n: o + abs(n[0] - n[1]), zip(listA, listB), 0)
print(res)
from functools import reduce

listA = list()
listB = list()

with open("input.txt", "r") as f:
    for l, r in map(lambda x: x.split(), f.readlines()):
        listA.append(int(l))
        listB.append(int(r))

# doubt this is even faster than count()
num = {}
for i in listB:
    num[i] = num.get(i, 0) + 1
res = reduce(lambda o, n: o + n * num.get(n, 0), listA, 0)
print(res)

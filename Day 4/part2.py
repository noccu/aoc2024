SEARCH_TERM = "MAS"
ANCHOR = SEARCH_TERM.index("A")


def get_input():
    with open("input.txt", "r") as f:
        return [l.strip() for l in f]


def probe(txt: list, iy: int, ix: int, dy: int, dx: int):
    search_range = [(iy + dy * i, ix + dx * i) for i in range(0, len(SEARCH_TERM))]
    try:
        letters = [
            txt[row][col]
            for row, col in search_range
            if row > -1 and col > -1
        ]  # fmt: skip
        return search_range, "".join(letters)
    except IndexError:
        return None, None


searches = (
    (-1, -1),  # up left
    (-1, 1),  # up right
    (1, -1),  # down left
    (1, 1),  # down right
)
txt = get_input()

found = set()
res = 0
for iy, row in enumerate(txt):
    for ix, _ in enumerate(row):
        for sy, sx in searches:
            r, p = probe(txt, iy, ix, sy, sx)
            if p == SEARCH_TERM:
                if r[ANCHOR] in found:
                    res += 1
                found.add(r[ANCHOR])


print(res)

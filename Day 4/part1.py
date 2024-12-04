SEARCH_TERM = "XMAS"


def get_input():
    with open("input.txt", "r") as f:
        return [l.strip() for l in f]


def probe(txt: list, iy: int, ix: int, dy: int, dx: int):
    search_range = ((iy + dy * i, ix + dx * i) for i in range(0, len(SEARCH_TERM)))
    try:
        letters = [
            txt[row][col]
            for row, col in search_range
            if row > -1 and col > -1
        ]  # fmt: skip
        return "".join(letters)
    except IndexError:
        return None


searches = (
    (0, 1),  # right
    (0, -1),  # left
    (-1, 0),  # up
    (-1, -1),  # up left
    (-1, 1),  # up right
    (1, 0),  # down
    (1, -1),  # down left
    (1, 1),  # down right
)
txt = get_input()

res = 0
for iy, row in enumerate(txt):
    for ix, _ in enumerate(row):
        for sy, sx in searches:
            if probe(txt, iy, ix, sy, sx) == SEARCH_TERM:
                res += 1
print(res)

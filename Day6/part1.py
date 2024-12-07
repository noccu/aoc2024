GUARD = "^"
OBSTACLE = "#"


def get_input():
    with open("input.txt", "r") as f:
        return [l.strip() for l in f]


def probe(txt: list, iy: int, ix: int, dy: int, dx: int):
    if dy == 0:
        size = ix + 1 if dx < 0 else len(txt[0]) - ix
    else:
        size = iy + 1 if dy < 0 else len(txt) - iy
    search_range = [(iy + dy * i, ix + dx * i) for i in range(0, size)]
    return list(filter(lambda x: x > (0, 0), search_range))


def walk_maze():
    pos: tuple
    dir = 0
    res = set()
    for y, row in enumerate(maze):
        for x, point in enumerate(row):
            if point == GUARD:
                pos = (y, x)

    while True:
        path = probe(maze, *pos, *searches[dir])
        has_obs = False
        for i, point in enumerate(path):
            if maze[point[0]][point[1]] == OBSTACLE:
                pos = path[i - 1]
                dir = (dir + 1) % len(searches)
                has_obs = True
                break
            res.add(point)
        if not has_obs:
            return res


searches = (
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
)
maze = get_input()

print(len(walk_maze()))

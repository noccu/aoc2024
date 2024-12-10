from time import process_time

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
    return tuple(filter(lambda x: x > (0, 0), search_range))


def match_point(maze, point, m, ovr=None):
    if ovr and point in ovr:
        return ovr[point] == m
    return maze[point[0]][point[1]] == m


def add_point(a, b):
    return (a[0] + b[0], a[1] + b[1])


def walk_path(maze, path, ovr, travel_log: set):
    for i, point in enumerate(path):
        travel_log.add(point)
        try:
            next_point = path[i + 1]
        except IndexError:
            return -1
        if match_point(maze, next_point, OBSTACLE, ovr):
            break
    return i


def walk_maze(start_pos, overrides=None):
    traveled = set()
    pos = start_pos
    dir = 0
    max_retraces = 5
    retraces = 0

    while True:
        path = probe(maze, *pos, *SEARCHES[dir])
        steps_before_walk = len(traveled)
        last_walkable_path_pos = walk_path(maze, path, overrides, traveled)
        if last_walkable_path_pos == -1:
            return True, traveled
        if len(traveled) == steps_before_walk:
            retraces += 1
        if retraces > max_retraces:
            return False, traveled
        pos = path[last_walkable_path_pos]
        dir = (dir + 1) % len(SEARCHES)


def get_start_pos(maze):
    for y, row in enumerate(maze):
        for x, point in enumerate(row):
            if point == GUARD:
                return (y, x)


SEARCHES = (
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
)
maze = get_input()
start_pos = get_start_pos(maze)
res = 0

start = process_time()
left_maze, patrol_route = walk_maze(start_pos)
assert left_maze
patrol_route.remove(start_pos)
for y, x in patrol_route:
    point = (y, x)
    if not walk_maze(start_pos, overrides={point: OBSTACLE})[0]:
        res += 1
end = process_time()
print(res)
print(f"Took: {end-start}s")

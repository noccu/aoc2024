from common.grids import Grid, Point
from time import process_time


def get_input():
    with open("input.txt", "r") as f:
        return Grid.parseInt(f)


def find_paths(grid: Grid, start_pt: Point, log: set):
    unique_paths = 0
    # print(f"Starting from {start_pt}: {start_val}")
    if grid.get(start_pt) == 9:
        # print(f"{start_pt} is the top!")
        log.add(start_pt)
        return 1
    for p in grid.neighbors(start_pt):
        # No early term for p2
        # if log and p in log:
        # print("Already found this top")
        # continue
        if grid.get(p) - grid.get(start_pt) != 1:
            continue
        # print(f"{p}: {grid.get(p)} is a valid next step")
        unique_paths += find_paths(grid, p, log)
    return unique_paths


start = process_time()
grid = get_input()
res_1 = 0
res_2 = 0
for root_pt, root_val in grid.walk():
    log = set()
    if root_val != 0:
        continue
    # print(f"Found a trailhead at {root_pt}")
    unique_paths = find_paths(grid, root_pt, log)
    res_1 += len(log)
    res_2 += unique_paths
end = process_time()
print(f"Part 1 (score - peaks reachable): {res_1}")
print(f"Part 2 (rating - unique paths): {res_2}")
print(f"Took: {end - start}s")

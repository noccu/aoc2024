from common.grids import Grid, DirectionsCardinal, Point, DirectionsDiagonal

type Region = dict[Point, str]

def get_input():
    with open("input.txt", "r") as f:
        return Grid.parseFromTextFile(f)


def calc(grid: Grid[str]):
    visited = set()
    cost = 0
    region_directory: dict[Point, Region] = dict()
    region_sides: dict[Point, int] = dict()
    # Find all regions
    for cur_pt, region_name in grid.walk():
        if cur_pt in visited:
            continue
        visited.add(cur_pt)
        region = find_region(grid, cur_pt, region_name, visited)
        region_directory[cur_pt] = region
    # Find all sides
    extra_sides: dict[Point, int] = dict()
    for root_pt, region in region_directory.items():
        walls, sur_pt = wall_walk(grid, region, root_pt)
        region_sides[root_pt] = walls
        # Calculate inner sides if present
        if sur_pt is not None:
            # print(f"Looking for root of {sur_pt}")
            # Find root of surrounding region
            for root, reg in region_directory.items():
                if sur_pt in reg:
                    cur_extra = extra_sides.get(root, 0)
                    extra_sides[root] = cur_extra + region_sides[root_pt]
                    # print(f"Found root at {root}, had {cur_extra}, added {region_sides[root_pt]}")
                    break
    # Calculate final side count and cost
    for root_pt, walls in region_sides.items():
        walls += extra_sides.get(root_pt, 0)
        print(f"Region {grid.get(root_pt)} at {root_pt} has {walls} sides")
        cost += walls * len(region_directory[root_pt])
    return cost


def wall_walk(grid: Grid[str], region: Region, start_pt: Point) -> tuple[int, Point|None]:
    start_dir = DirectionsCardinal.UP
    cur_pt = start_pt
    cur_dir = start_dir
    first_time = True
    walls = 0
    surrounding_region = dict()

    while first_time or (cur_pt != start_pt or cur_dir != start_dir):
        # print(f"Starting in {cur_dir}!") if first_time else print(f"Direction changed to {cur_dir}")
        first_time = False
        prev_dir = DirectionsCardinal.step(cur_dir, -1)
        next_dir = DirectionsCardinal.step(cur_dir, 1)
        prev_pt = cur_pt + prev_dir
        next_pt = cur_pt + next_dir
        target_pt = cur_pt + cur_dir
        for p in tuple(grid.unsafe_neighbors(cur_pt)) + tuple(
            cur_pt + d for d in DirectionsDiagonal.LIST
        ):
            if p not in region:
                val = grid.get(p) if grid.is_valid_coord(p) else "OOB"
                surrounding_region[val] = p
        # region already filtered to be in bounds
        if prev_pt in region:
            cur_pt = prev_pt
            cur_dir = prev_dir
            walls += 1
            # print(f"Moved prev {cur_pt}")
        elif target_pt in region:
            cur_pt = target_pt
            # print(f"Moved target {cur_pt}")
        elif next_pt in region:
            cur_pt = next_pt
            cur_dir = next_dir
            walls += 1
            # print(f"Moved next {cur_pt}")
        else:
            cur_dir = next_dir
            walls += 1
            # print(f"No move, change dir. Still {cur_pt}")
    if len(surrounding_region) == 1:
        k, v = next(iter(surrounding_region.items()))
        print(f"Surrounding set ({k}) found!")
        surrounding_region = v
    else:
        surrounding_region = None
    return walls, surrounding_region


def find_region(grid: Grid[str], cur_pt: Point, region_name: str, visited: set):
    region = {cur_pt: region_name}
    for neighbor_pt in grid.neighbors(cur_pt):
        neighbor_region_name = grid.get(neighbor_pt)
        if neighbor_region_name != region_name or neighbor_pt in visited:
            continue
        visited.add(neighbor_pt)
        region.update(find_region(grid, neighbor_pt, neighbor_region_name, visited))
    return region


grid = get_input()
print(calc(grid))

from common.grids import Grid, GridCel, DirectionsCardinal, Point, DirectionsDiagonal

TEST_RESULT_1 = 140


def get_input():
    with open("input.txt", "r") as f:
        return Grid.parseToType(GridCel, f)


def build_graph(grid: Grid):
    for p, val in grid.walk():
        for p in grid.neighbors(p):
            n_val = grid.get(p)
            val.addChild(n_val)


def calc(grid: Grid):
    visited = set()
    cost = 0
    region_directory = dict()
    region_sides = dict()
    # find all regions
    for cur_pt, cur_node in grid.walk():
        if cur_pt in visited:
            continue
        visited.add(cur_pt)
        region = find_region(grid, cur_pt, cur_node, visited)
        region_directory[cur_pt] = region
    # Find all sides
    extra_sides = dict()
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


def wall_walk(grid: Grid, region: dict[Point, GridCel], start_pt):
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
        behind_dir = DirectionsCardinal.step(cur_dir, +2)
        while True:
            prev_pt = cur_pt + prev_dir
            next_pt = cur_pt + next_dir
            behind_pt = cur_pt + behind_dir
            target_pt = cur_pt + cur_dir
            for p in (prev_pt, next_pt, target_pt, behind_pt) + tuple(
                cur_pt + d for d in DirectionsDiagonal.LIST
            ):
                if p not in region:
                    val = grid.get(p).value if grid.is_valid_coord(p) else "OOB"
                    surrounding_region[val] = p
            # region already filtered to be in bounds
            if prev_pt in region:
                cur_pt = prev_pt
                cur_dir = prev_dir
                walls += 1
                break
                # print(f"Moved prev {cur_pt}")
            elif target_pt in region:
                cur_pt = target_pt
                break
                # print(f"Moved target {cur_pt}")
            elif next_pt in region:
                cur_pt = next_pt
                cur_dir = next_dir
                walls += 1
                # print(f"Moved next {cur_pt}")
                break
            else:
                cur_dir = next_dir
                walls += 1
                # print(f"No move, change dir. Still {cur_pt}")
                break
    if len(surrounding_region) == 1:
        for k, v in surrounding_region.items():
            print(f"Surrounding set ({k}) found!")
            surrounding_region = v
    else:
        surrounding_region = None
    return walls, surrounding_region


def find_region(grid: Grid, cur_pt: Point, cur_node: GridCel, visited: set):
    region = {cur_pt: cur_node}
    for neighbor_pt in grid.neighbors(cur_pt):
        neighbor_node = grid.get(neighbor_pt)
        if neighbor_node.value != cur_node.value or neighbor_pt in visited:
            continue
        visited.add(neighbor_pt)
        region.update(find_region(grid, neighbor_pt, neighbor_node, visited))
    return region


grid = get_input()
build_graph(grid)
print(calc(grid))

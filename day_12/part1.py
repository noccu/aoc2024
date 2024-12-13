from common.grids import Grid, Point


def get_input():
    with open("test_input.txt", "r") as f:
        return Grid.parseFromTextFile(f)


def calc(grid: Grid[str]):
    visited = set()
    cost = 0
    for cur_pt, cur_node in grid.walk():
        if cur_pt in visited:
            continue
        visited.add(cur_pt)
        region = find_region(grid, cur_pt, cur_node, visited)
        perim = 0
        for n in region:
            perim += sum(1 for n in grid.unsafe_neighbors(n) if n not in region)
        # print(f"Region {cur_node}: perim {perim}, cost: {perim * len(region)}")
        cost += perim * len(region)
    return cost


def find_region(grid: Grid[str], cur_pt: Point, region_name: str, visited: set):
    region = [cur_pt]
    for neighbor_pt in grid.neighbors(cur_pt):
        neighbor_region_name = grid.get(neighbor_pt)
        if neighbor_region_name != region_name or neighbor_pt in visited:
            continue
        visited.add(neighbor_pt)
        region.extend(find_region(grid, neighbor_pt, neighbor_region_name, visited))
    return region


grid = get_input()
print(calc(grid))

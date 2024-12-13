from common.grids import Grid, NodeUndirected, Point


def get_input():
    with open("input.txt", "r") as f:
        return Grid.parseToType(NodeUndirected, f)


def build_graph(grid: Grid):
    for p, val in grid.walk():
        for p in grid.neighbors(p):
            n_val = grid.get(p)
            val.link(n_val)


def calc(grid: Grid):
    visited = set()
    cost = 0
    for cur_pt, cur_node in grid.walk():
        if cur_pt in visited:
            continue
        visited.add(cur_pt)
        region = find_region(grid, cur_pt, cur_node, visited)
        perim = 0
        for n in region:
            e = tuple(filter(lambda x: x in region, n.links))
            perim += 4 - len(e)
        # print(f"Region {n.value}: perim {perim}, cost: {perim * len(region)}")
        cost += perim * len(region)
    return cost


def find_region(grid: Grid, cur_pt: Point, cur_node:NodeUndirected, visited:set):
    region = [cur_node]
    for neighbor_pt in grid.neighbors(cur_pt):
        neighbor_node = grid.get(neighbor_pt)
        if neighbor_node.value != cur_node.value or neighbor_pt in visited:
            continue
        visited.add(neighbor_pt)
        region.extend(find_region(grid, neighbor_pt, neighbor_node, visited))
    return region


grid = get_input()
build_graph(grid)
print(calc(grid))
# print(grid)

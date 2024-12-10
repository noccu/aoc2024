from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    type: str

    def project(self, n: "Node"):
        vx = n.x - self.x
        vy = n.y - self.y
        return (n.x + vx, n.y + vy)

    def is_oob(self, map_size: "Node"):
        if not (0 <= self.x <= map_size.x) or not (0 <= self.y <= map_size.y):
            return True
        return False


def get_input():
    with open("input.txt", "r") as f:
        return (l.strip() for l in f.readlines())


def parse_map():
    nodes: list[Node] = list()
    for y, row in enumerate(get_input()):
        for x, t in enumerate(row):
            if t != ".":
                nodes.append(Node(x, y, t))
    return nodes, Node(x, y, "map")


nodes, map_size = parse_map()
antinodes = set()
for n in nodes:
    for nn in nodes:
        if nn == n or n.type != nn.type:
            continue
        antinode = Node(*n.project(nn), "anti")
        if not antinode.is_oob(map_size):
            antinodes.add(antinode)
print(len(antinodes))

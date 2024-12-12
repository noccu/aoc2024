from .points import Point
from collections.abc import Iterator
# from collections import deque


class DirectionsCardinal:
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    LIST = (UP, RIGHT, DOWN, LEFT)

    @classmethod
    def iter(cls):
        return cls.LIST

    @classmethod
    def iter_adv(cls, reverse=False, start=None):
        # return reversed(cls.LIST) if reverse else iter(cls.LIST)
        s_idx = cls.LIST.index(start) if start else 0
        for i in range(s_idx, start, -1) if reverse else range(start, s_idx):
            yield cls.LIST[i]


class Grid:
    def __init__(self, grid: list):
        self.grid = grid
        self.w = len(grid[0])
        self.h = len(grid)

    def is_valid_coord(self, p: Point):
        if not len(self.grid):
            return False
        return 0 <= p.x < len(self.grid[0]) and 0 <= p.y < len(self.grid)

    def get(self, x: int | Point, y=None):
        if isinstance(x, Point):
            return self.grid[x.y][x.x]
        return self.grid[y][x]

    def neighbors(self, pt: Point) -> Iterator[Point]:
        return filter(self.is_valid_coord, (pt + p for p in DirectionsCardinal.iter()))

    def walk(self):
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                yield Point(x, y), val

    # def bfs_pt(self, root: Point, max=None):
    #     q: deque[Point] = deque((root), max)
    #     visited = set()  # fast
    #     path = list()  # ordered
    #     point = root
    #     while q:
    #         point = q.popleft()
    #         visited.add(point)
    #         path.append(point)
    #         yield point
    #         for neighbor in self.neighbors(point):
    #             if neighbor not in visited:
    #                 q.append(neighbor)
    #     return point, path

    # def bfs(root: Node, f_valid, f_target, max=None):
    #     q: deque[Node] = deque((root), max)
    #     visited = set()
    #     while q:
    #         node = q.popleft()
    #         if f_target(node):
    #             break
    #         visited.add(node)
    #         for c in node.children:
    #             if c not in visited and f_valid(root, node):
    #                 q.append(c)

    @classmethod
    def parseInt(cls, txt):
        return cls([list(map(int, l.strip())) for l in txt])

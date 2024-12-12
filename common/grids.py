from .points import Point
from collections.abc import Iterator
from typing import Self
from dataclasses import dataclass, field
# from collections import deque


class DirectionsDiagonal:
    UP_LEFT = Point(-1, -1)
    UP_RIGHT = Point(-1, 1)
    DOWN_LEFT = Point(1, -1)
    DOWN_RIGHT = Point(1, 1)
    LIST = (UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT)


class DirectionsCardinal:
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    LIST = (UP, RIGHT, DOWN, LEFT)

    @classmethod
    def step(cls, start, step):
        s = cls.LIST.index(start)
        return cls.LIST[(s + step) % len(cls.LIST)]

    @classmethod
    def rotate(cls, reverse=False, start=None):
        # return reversed(cls.LIST) if reverse else iter(cls.LIST)
        s_idx = cls.LIST.index(start) if start else 0
        for i in range(s_idx, start, -1) if reverse else range(start, s_idx):
            return cls.LIST[i]

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

    def set(self, val, x: int | Point, y=None):
        if isinstance(x, Point):
            self.grid[x.y][x.x] = val
        else:
            self.grid[y][x] = val
        return val

    def neighbors(self, pt: Point) -> Iterator[Point]:
        return filter(self.is_valid_coord, (pt + p for p in DirectionsCardinal.iter()))

    def unsafe_neighbors(self, pt: Point) -> Iterator[Point]:
        return (pt + p for p in DirectionsCardinal.iter())

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
    def parseStr(cls, txt):
        return cls([list(l.strip()) for l in txt])

    @classmethod
    def parseInt(cls, txt):
        return cls([list(map(int, l.strip())) for l in txt])

    @classmethod
    def parseToType(cls, t, txt):
        return cls([list(map(t, l.strip())) for l in txt])


@dataclass
class GridCel:
    value: any
    parents: list[Self] = field(init=False, default_factory=list)
    children: list[Self] = field(init=False, default_factory=list)

    def addChild(self, node: Self):
        for n in self.children:
            n.parents.append(self)
        self.children.append(node)
        return node

    def addParent(self, node: Self):
        for n in self.parents:
            n.children.append(self)
        self.parents.append(node)
        return node

    # def delete(self):
    #     self.children.remove(self)
    #     self.parents.remove(self)

    def __repr__(self):
        return f"[Node {self.value}]"

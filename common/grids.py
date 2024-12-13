from .points import Point
from collections.abc import Iterator, Iterable, Callable
from typing import TextIO
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


type GridInput[T] = Iterable[Iterable[T]]
type TypeConstructor[T] = Callable[..., T]


class Grid[T]:
    def __init__(self, grid: GridInput[T]):
        self.grid = [list(row) for row in grid]
        self.w = len(self.grid[0])
        self.h = len(self.grid)

    def is_valid_coord(self, p: Point):
        if not len(self.grid):
            return False
        return 0 <= p.x < len(self.grid[0]) and 0 <= p.y < len(self.grid)

    def get(self, x: int | Point, y: int = None):
        if isinstance(x, Point):
            return self.grid[x.y][x.x]
        return self.grid[y][x]

    def set(self, val, x: int | Point, y: int = None):
        if isinstance(x, Point):
            self.grid[x.y][x.x] = val
        else:
            self.grid[y][x] = val
        return val

    def neighbors(self, pt: Point) -> Iterator[Point]:
        return filter(self.is_valid_coord, self.unsafe_neighbors(pt))

    def unsafe_neighbors(self, pt: Point) -> Iterator[Point]:
        return (pt + p for p in DirectionsCardinal.iter())

    def walk(self):
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                yield Point(x, y), val

    @classmethod
    def parse[I, T](cls, txt: GridInput[I], toType: TypeConstructor[T] | None = None) -> "Grid[T|I]":
        if toType is None:
            return cls(txt)
        return cls(map(toType, l) for l in txt)

    @classmethod
    def parseFromTextFile[T](cls, f: TextIO, toType: TypeConstructor[T] | None = None):
        return cls.parse((l.strip() for l in f), toType)

    def __repr__(self):
        return "\n".join(str(row) for row in self.grid)

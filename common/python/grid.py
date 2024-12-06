from enum import Enum
from nis import match
from typing import List

class GridVector:
    i: int = 0
    j: int = 0

    def __init__(self, i, j):
        self.i = i
        self.j = j

class GridPoint:
    i: int = 0
    j: int = 0

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def move(self, vec: GridVector):
        return GridPoint(self.i + vec.i, self.j + vec.j)


# class syntax

class Direction(Enum):
    UP = GridVector(-1, 0)
    DOWN = GridVector(1, 0)
    LEFT = GridVector(0, -1)
    RIGHT = GridVector(0, 1)

    def rotate_clockwise(self):
        # Could do math here, but don't want
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.LEFT
        return Direction.UP


def is_in_bounds(grid: List[List[str]], point: GridPoint) -> bool:
    if point.i < 0 or point.i >= len(grid):
        return False
    if point.j < 0 or point.j >= len(grid[point.i]):
        return False

    return True
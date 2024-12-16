from enum import Enum
from typing import List

class GridVector:
    i: int = 0
    j: int = 0

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def multiply(self, x: int) -> 'GridVector':
        return GridVector(self.i * x, self.j * x)

    def add(self, x: 'GridVector') -> 'GridVector':
        return GridVector(self.i + x.i, self.j + x.j)

    def __str__(self):
        return f'[{self.i},{self.j}]'

class GridPoint:
    i: int = 0
    j: int = 0

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def move(self, vec: GridVector):
        return GridPoint(self.i + vec.i, self.j + vec.j)

    def as_str(self) -> str:
        return "(" + str(self.i) + "," + str(self.j) + ")"

    def __str__(self):
        self.as_str()

    def vector_to(self, b) -> GridVector:
        return GridVector(b.i - self.i, b.j - self.j)


# class syntax

class Direction(Enum):
    UP = GridVector(-1, 0)
    DOWN = GridVector(1, 0)
    LEFT = GridVector(0, -1)
    RIGHT = GridVector(0, 1)

    def rotate_clockwise(self) -> 'Direction':
        # Could do math here, but don't want
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.LEFT
        return Direction.UP

    def rotate_anticlockwise(self) -> 'Direction':
        if self == Direction.UP:
            return Direction.LEFT
        if self == Direction.RIGHT:
            return Direction.UP
        if self == Direction.DOWN:
            return Direction.RIGHT
        return Direction.DOWN

    def as_str(self) -> str:
        if self == Direction.UP:
            return "^"
        if self == Direction.RIGHT:
            return ">"
        if self == Direction.DOWN:
            return "v"
        return "<"


def is_in_bounds(grid: List[List], point: GridPoint) -> bool:
    if point.i < 0 or point.i >= len(grid):
        return False
    if point.j < 0 or point.j >= len(grid[point.i]):
        return False

    return True

def points_in_grid(grid: List[List]):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            yield GridPoint(i, j)

def get_directly_adjacent(grid: List[List], point: GridPoint) -> List[GridPoint]:
    directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    output = []
    for direction in directions:
        adjacent = point.move(direction.value)
        if is_in_bounds(grid, adjacent):
            output.append(adjacent)

    return output

def print_points_on_grid(grid: List[List], points: List[GridPoint]):
    out_grid = []

    for line in grid:
        out_grid.append(["." for _ in line])

    for point in points:
        out_grid[point.i][point.j] = "X"

    for line in out_grid:
        print("".join(line))

def print_grid(grid: List[List[str]]):
    for line in grid:
        print("".join(line))

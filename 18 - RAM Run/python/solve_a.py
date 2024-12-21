import os
import re
from typing import List, Union

from grid import GridPoint, get_directly_adjacent
from loader import input_as_strings


class EscapeePosition:
    def __init__(self, point: GridPoint, score: int):
        self.point = point
        self.score = score

class EmptyPosition:
    best = None

    def record(self, score: int) -> bool:
        if self.best is None or score < self.best:
            self.best = score
            return True

        return False

class CorruptedPosition:
    def record(self, score: int):
        # Can't go to a corrupted position
        return False

if __name__ == "__main__":
    input = input_as_strings()

    is_example = os.getenv('AOC_EXAMPLE_MODE') == "1"
    grid_size = 7 if is_example else 71

    board: List[List[Union[EmptyPosition, CorruptedPosition]]] = []
    for _ in range(0, grid_size):
        line = []
        for _ in range(0, grid_size):
            line.append(EmptyPosition())
        board.append(line)

    bytes_to_read = 12 if is_example else 1024
    for b in range(0, bytes_to_read):
        byte_line = input[b]
        coords = [int(x) for x in re.findall('[0-9]+', byte_line)]
        corrupt_point = GridPoint(coords[0], coords[1])
        board[corrupt_point.i][corrupt_point.j] = CorruptedPosition()

    frontier = [EscapeePosition(GridPoint(0,0), 0)]
    while len(frontier) > 0:
        new_frontier = []
        for position in frontier:
            point = position.point
            location = board[point.i][point.j]
            if not location.record(position.score):
                # Not an improvement
                continue

            adjacent = [EscapeePosition(p, position.score + 1) for p in get_directly_adjacent(board, point)]
            new_frontier = new_frontier + adjacent

        frontier = new_frontier

    score = board[grid_size - 1][grid_size - 1].best
    print(score)
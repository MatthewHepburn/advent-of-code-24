from typing import List, Union, Optional

from grid import GridPoint, get_directly_adjacent


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

BoardType = List[List[Union[EmptyPosition, CorruptedPosition]]]

def get_best_route_length(board: BoardType) -> Optional[int]:
    frontier = [EscapeePosition(GridPoint(0, 0), 0)]
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

    return board[len(board) - 1][len(board) - 1].best
from typing import List, Optional

from grid import GridPoint, Direction, is_in_bounds, get_directly_adjacent, points_in_grid
from loader import input_as_chars_trimmed

# Cheat states:
# 0 - not cheated
# 1 - in first move of cheat
# 2 - in second move of cheat
# 3 - cheat ended, cannot cheat again

class RacerPosition:
    def __init__(self, point: GridPoint, cheat_state: int):
        self.point = point
        self.cheat_state = cheat_state

class EmptyPosition:
    best = None
    is_wall = False

    def record(self, score: int) -> bool:
        if self.best is None or score < self.best:
            self.best = score
            return True

        return False

class WallPosition:
    is_wall = True

    def record(self, score: int):
        # Can't go to a wall
        return False

def get_start_position(board: List[List[str]]) -> GridPoint:
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 'S':
                return GridPoint(i, j)

    raise Exception("Could not find start")

def get_end_position(board: List[List[str]]) -> GridPoint:
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 'E':
                return GridPoint(i, j)

    raise Exception("Could not find start")

if __name__ == "__main__":
    input = input_as_chars_trimmed()

    start = get_start_position(input)
    end_point = get_end_position(input)

    # TODO - reverse start and end so we have distance to end at every point
    # We can then assess the saving of every possible cheat by looking at the distance saving

    board = []
    for line in input:
        board.append([WallPosition() if c == "#" else EmptyPosition() for c in line])

    end_position = board[end_point.i][end_point.j]

    frontier = [start]
    steps = 0
    while len(frontier) > 0:
        new_frontier = []
        for point in frontier:
            location = board[point.i][point.j]
            if not location.record(steps):
                # Not an improvement
                continue

            new_frontier = new_frontier + get_directly_adjacent(board, point)

        steps = steps + 1
        frontier = new_frontier

    # Need to know how long the course takes without cheats to know how much a cheat saves
    control_time = score = board[end_point.i][end_point.j].best

    for point in points_in_grid(board):
        if board[point.i][point.j].is_wall:
            continue


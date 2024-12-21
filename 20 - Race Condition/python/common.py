from typing import List

from grid import GridPoint


class EmptyPosition:
    distance_from_start = None
    distance_from_end = None
    is_wall = False

    def record_from_start(self, distance: int) -> bool:
        if self.distance_from_start is None or distance < self.distance_from_start:
            self.distance_from_start = distance
            return True

        return False

    def record_from_end(self, distance: int) -> bool:
        if self.distance_from_end is None or distance < self.distance_from_end:
            self.distance_from_end = distance
            return True

        return False


class WallPosition:
    is_wall = True

    def record_from_start(self, distance: int):
        # Can't go to a wall
        return False

    def record_from_end(self, distance: int):
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
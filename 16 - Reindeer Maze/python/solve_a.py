from typing import List, Optional

from grid import GridPoint, Direction, is_in_bounds
from loader import input_as_chars_trimmed


class ReindeerPosition:
    def __init__(self, point: GridPoint, direction: Direction, score: int):
        self.point = point
        self.direction = direction
        self.score = score

class EmptyPosition:
    best_up = None
    best_left = None
    best_right = None
    best_down = None

    def record(self, position: ReindeerPosition) -> bool:
        direction = position.direction
        cur_best = self.get_current_for_direction(direction)
        if cur_best is None or position.score < cur_best:
            self.set_for_direction(direction, position.score)
            return True

        return False

    def get_current_for_direction(self, direction: Direction) -> Optional[int]:
        if direction == Direction.UP:
            return self.best_up
        if direction == Direction.LEFT:
            return self.best_left
        if direction == Direction.RIGHT:
            return self.best_right
        if direction == Direction.DOWN:
            return self.best_down

    def set_for_direction(self, direction: Direction, score: int):
        if direction == Direction.UP:
            self.best_up = score
        if direction == Direction.LEFT:
            self.best_left = score
        if direction == Direction.RIGHT:
            self.best_right = score
        if direction == Direction.DOWN:
            self.best_down = score

class WallPosition:
    def record(self, position: ReindeerPosition):
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

    start = ReindeerPosition(get_start_position(input), Direction.RIGHT, 0)
    end_point = get_end_position(input)

    board = []
    for line in input:
        board.append([WallPosition() if c == "#" else EmptyPosition() for c in line])

    end_position = board[end_point.i][end_point.j]

    frontier = [start]
    while len(frontier) > 0:
        new_frontier = []
        for position in frontier:
            point = position.point
            location = board[point.i][point.j]
            if not location.record(position):
                # Not an improvement
                continue

            forward = point.move(position.direction.value)
            if is_in_bounds(board, forward):
                new_frontier.append(ReindeerPosition(forward, position.direction, position.score + 1))

            # Can always rotate
            new_frontier.append(ReindeerPosition(point, position.direction.rotate_clockwise(), position.score + 1000))
            new_frontier.append(ReindeerPosition(point, position.direction.rotate_clockwise().rotate_clockwise(), position.score + 2000))
            new_frontier.append(ReindeerPosition(point, position.direction.rotate_anticlockwise(), position.score + 1000))

        frontier = new_frontier

    score = min(end_position.best_up, end_position.best_down, end_position.best_right, end_position.best_down)
    print(score)
from copy import copy
from typing import List, Optional

from grid import GridPoint, Direction, is_in_bounds, print_points_on_grid
from loader import input_as_chars_trimmed


class ReindeerPosition:
    def __init__(self, point: GridPoint, direction: Direction, score: int, path: List[GridPoint]):
        self.point = point
        self.direction = direction
        self.score = score
        self.path = path

class EmptyPosition:
    is_wall: bool = False

    best_up = None
    best_left = None
    best_right = None
    best_down = None

    best_up_paths = []
    best_left_paths = []
    best_right_paths = []
    best_down_paths = []

    def record(self, position: ReindeerPosition) -> bool:
        direction = position.direction
        cur_best = self.get_current_for_direction(direction)
        if cur_best is None or position.score < cur_best:
            self.set_for_direction(direction, position.score, position.path)
            return True
        elif position.score == cur_best:
            self.add_for_direction(direction, position.path)
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

    def set_for_direction(self, direction: Direction, score: int, path: List[GridPoint]):
        if direction == Direction.UP:
            self.best_up = score
            self.best_up_paths = [path]
        if direction == Direction.LEFT:
            self.best_left = score
            self.best_left_paths = [path]
        if direction == Direction.RIGHT:
            self.best_right = score
            self.best_right_paths = [path]
        if direction == Direction.DOWN:
            self.best_down = score
            self.best_down_paths = [path]

    def add_for_direction(self, direction: Direction, path: List[GridPoint]):
        if direction == Direction.UP:
            self.best_up_paths.append(path)
        if direction == Direction.LEFT:
            self.best_left_paths.append(path)
        if direction == Direction.RIGHT:
            self.best_right_paths.append(path)
        if direction == Direction.DOWN:
            self.best_down_paths.append(path)

class WallPosition:
    is_wall: bool = True

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

    start = ReindeerPosition(get_start_position(input), Direction.RIGHT, 0, [])
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
            if is_in_bounds(board, forward) and not board[forward.i][forward.j].is_wall:
                new_path = copy(position.path)
                new_path.append(point)
                new_frontier.append(ReindeerPosition(forward, position.direction, position.score + 1, new_path))

            # Can always rotate
            new_frontier.append(ReindeerPosition(point, position.direction.rotate_clockwise(), position.score + 1000, copy(position.path)))
            new_frontier.append(ReindeerPosition(point, position.direction.rotate_clockwise().rotate_clockwise(), position.score + 2000, copy(position.path)))
            new_frontier.append(ReindeerPosition(point, position.direction.rotate_anticlockwise(), position.score + 1000, copy(position.path)))

        frontier = new_frontier
        # print("Len(frontier) = ", len(frontier))

    score = min(end_position.best_up, end_position.best_down, end_position.best_right, end_position.best_down)
    best_paths = []
    if score == end_position.best_up:
        best_paths = best_paths + end_position.best_up_paths
    if score == end_position.best_down:
        best_paths = best_paths + end_position.best_down_paths
    if score == end_position.best_left:
        best_paths = best_paths + end_position.best_left_paths
    if score == end_position.best_right:
        best_paths = best_paths + end_position.best_right_paths

    good_points = set()
    good_points.add(start.point.as_str())
    good_points.add(end_point.as_str())

    # points_to_draw = [start.point, end_point]

    for path in best_paths:
        for point in path:
            good_points.add(point.as_str())
            # points_to_draw.append(point)

    # print_points_on_grid(board, points_to_draw)
    print(len(good_points))
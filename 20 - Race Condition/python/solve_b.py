from typing import List, Union

from common import EmptyPosition, WallPosition, get_start_position, get_end_position
from grid import GridPoint, is_in_bounds, get_directly_adjacent, points_in_grid, GridVector
from loader import input_as_chars_trimmed

def get_cheat_points(board: List[List[Union[EmptyPosition, WallPosition]]], point: GridPoint) -> List[GridPoint]:
    points = []
    for i in range(-20, 21):
        for j in range(-20, 21):
            if abs(i) + abs(j) < 1 or abs(i) + abs(j) > 20:
                continue
            candidate_point = point.move(GridVector(i, j))
            if not is_in_bounds(board, candidate_point):
                continue
            if board[candidate_point.i][candidate_point.j].is_wall:
                continue
            points.append(candidate_point)

    return points

if __name__ == "__main__":
    input = input_as_chars_trimmed()

    start = get_start_position(input)
    end_point = get_end_position(input)

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
            if not location.record_from_start(steps):
                # Not an improvement
                continue

            new_frontier = new_frontier + get_directly_adjacent(board, point)

        steps = steps + 1
        frontier = new_frontier

    # Need to know how long the course takes without cheats to know how much a cheat saves
    control_distance = board[end_point.i][end_point.j].distance_from_start

    # Work in reverse, record the distance of each point from the end
    frontier = [end_point]
    steps = 0
    while len(frontier) > 0:
        new_frontier = []
        for point in frontier:
            location = board[point.i][point.j]
            if not location.record_from_end(steps):
                # Not an improvement
                continue

            new_frontier = new_frontier + get_directly_adjacent(board, point)

        steps = steps + 1
        frontier = new_frontier

    # Now, assess all possible cheats
    cheats_by_savings = dict()

    for point in points_in_grid(board):
        start_position = board[point.i][point.j]
        if start_position.is_wall:
            continue

        for end_point in get_cheat_points(board, point):
            end_position = board[end_point.i][end_point.j]
            cheat_distance = abs(end_point.i - point.i) + abs(end_point.j - point.j)
            distance = cheat_distance + start_position.distance_from_start + end_position.distance_from_end
            saving = control_distance - distance
            if saving < 50:
                continue
            count = 1 if saving not in cheats_by_savings else cheats_by_savings[saving] + 1
            cheats_by_savings[saving] = count

    # Output in example format as test:
    possible_savings = list(cheats_by_savings.keys())
    possible_savings.sort()
    for possible_saving in possible_savings:
        count = cheats_by_savings[possible_saving]
        if count > 1:
            print(f"There are {count} cheats that save {possible_saving} picoseconds")
        else:
            print(f"There is one cheat that saves {possible_saving} picoseconds")

    total = 0
    for saving, count in cheats_by_savings.items():
        if saving >= 100:
            total = total + count

    print(total)



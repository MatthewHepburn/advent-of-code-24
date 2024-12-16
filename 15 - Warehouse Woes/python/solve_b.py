from typing import List

from common import direction_from_symbol
from grid import Direction, GridPoint, GridVector, points_in_grid
from loader import input_as_strings
from enum import Enum

class MapItem(Enum):
    EMPTY = "."
    WALL = "#"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    ROBOT = "@"

    def from_str(input: str) -> "MapItem":
        if input == "#":
            return MapItem.WALL
        if input == ".":
            return  MapItem.EMPTY
        if input == "[":
            return MapItem.BOX_LEFT
        if input == "]":
            return MapItem.BOX_RIGHT
        if input == "@":
            return MapItem.ROBOT
        raise Exception("Unknown MapItem input: '" + input + "'")

def print_board(board: List[List[MapItem]]):
    for line in board:
        print("".join([x.value for x in line]))

def get_robot_position(board: List[List[MapItem]]) -> GridPoint:
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == MapItem.ROBOT:
                return GridPoint(i, j)

    raise Exception("Could not find robot")

def get_gps_score(board: List[List[MapItem]]) -> int:
    score = 0
    for point in points_in_grid(board):
        if board[point.i][point.j] == MapItem.BOX_LEFT:
            score += (100 * point.i) + point.j

    return score


def expand(c: str) -> str:
    if c == "@":
        return "@."
    if c == "O":
        return "[]"
    return c + c


if __name__ == "__main__":
    input = input_as_strings()

    board = []
    moves = []
    for line in input:
        if "." in line or "#" in line:
            expanded_line = "".join([expand(c) for c in list(line.strip())])
            board.append([MapItem.from_str(c) for c in list(expanded_line)])
        else:
            moves = moves + [direction_from_symbol(c) for c in list(line.strip())]

    # print_board(board)

    position = get_robot_position(board)
    # print("Position = ", position.as_str())

    for move in moves:
        box_points_pairs_to_move: List[List[GridPoint]] = []
        wall_in_way = False
        move_vec: GridVector = move.value
        frontier = [position.move(move_vec)]
        # print("Move = ", move.as_str())
        while frontier:
            # print([x.as_str() for x in frontier])
            new_frontier = []
            for point in frontier:
                value = board[point.i][point.j]
                if value == MapItem.WALL:
                    wall_in_way = True
                    frontier = []
                    break
                if value == MapItem.BOX_LEFT or value == MapItem.BOX_RIGHT:
                    box_points = []
                    if value == MapItem.BOX_LEFT:
                        box_points = [point, point.move(GridVector(0, 1))]
                    else:
                        box_points = [point.move(GridVector(0, -1)), point]

                    # print("Found a box: ", value.value, " Point = ", [x.as_str() for x in box_points])

                    if move == Direction.UP or move == Direction.DOWN:
                        # Check both squares above/below
                        new_frontier = new_frontier + [box_points[0].move(move_vec), box_points[1].move(move_vec)]
                    elif move == Direction.LEFT:
                        # Only check left
                        new_frontier.append(box_points[0].move(move_vec))
                    else:
                        # Only check right
                        new_frontier.append(box_points[1].move(move_vec))

                    box_points_pairs_to_move.append(box_points)

            frontier = new_frontier

        if wall_in_way:
            continue

        for box_point_pair in box_points_pairs_to_move:
            for box_point in box_point_pair:
                # Erase all existing boxes
                board[box_point.i][box_point.j] = MapItem.EMPTY
        for box_point_pair in box_points_pairs_to_move:
            left = box_point_pair[0].move(move_vec)
            right = box_point_pair[1].move(move_vec)
            board[left.i][left.j] = MapItem.BOX_LEFT
            board[right.i][right.j] = MapItem.BOX_RIGHT

        # Remove and replace the robot
        board[position.i][position.j] = MapItem.EMPTY
        position = position.move(move.value)
        board[position.i][position.j] = MapItem.ROBOT

        # print("-----------Moved " + move.as_str() + "---------------")
        # print_board(board)

    print(get_gps_score(board))

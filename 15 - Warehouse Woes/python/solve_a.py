from typing import List

from grid import Direction, GridPoint, GridVector, points_in_grid
from loader import input_as_strings
from enum import Enum

class MapItem(Enum):
    EMPTY = "."
    WALL = "#"
    BOX = "O"
    ROBOT = "@"

    def from_str(input: str) -> "MapItem":
        if input == "#":
            return MapItem.WALL
        if input == ".":
            return  MapItem.EMPTY
        if input == "O":
            return MapItem.BOX
        if input == "@":
            return MapItem.ROBOT
        raise Exception("Unknown MapItem input: '" + input + "'")

def direction_from_symbol(input: str) -> Direction:
    if input == ">":
        return Direction.RIGHT
    if input == "^":
        return Direction.UP
    if input == "<":
        return Direction.LEFT
    if input == "v":
        return Direction.DOWN
    raise Exception("Unknown Direction input: " + input)

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
        if board[point.i][point.j] == MapItem.BOX:
            score += (100 * point.i) + point.j

    return score

if __name__ == "__main__":
    input = input_as_strings()

    board = []
    moves = []
    for line in input:
        if "." in line or "#" in line:
            board.append([MapItem.from_str(c) for c in list(line.strip())])
        else:
            moves = moves + [direction_from_symbol(c) for c in list(line.strip())]

    # print_board(board)
    # print("Got " + str(len(moves)) + " moves")

    position = get_robot_position(board)
    # print("Position = ", position.as_str())

    for move in moves:
        adjacent_boxes = []
        wall_in_way = False
        last = None
        vec: GridVector = GridVector(0,0)
        while last != MapItem.EMPTY:
            vec = vec.add(move.value)
            last_pos = position.move(vec)
            last = board[last_pos.i][last_pos.j]
            if last == MapItem.WALL:
                wall_in_way = True
                break
            if last == MapItem.BOX:
                adjacent_boxes.append(last_pos)


        if wall_in_way:
            # print("Cannot move " + move.as_str() + " - wall in way")
            continue

        # Put a box at robot + vec, if we have one to move
        if len(adjacent_boxes) > 0:
            new_box_pos = position.move(vec)
            # sanity check
            if board[new_box_pos.i][new_box_pos.j] != MapItem.EMPTY:
                raise Exception("Logic error - cannot move box to non-empty space")
            board[new_box_pos.i][new_box_pos.j] = MapItem.BOX

        # Remove the robot
        board[position.i][position.j] = MapItem.EMPTY

        # Place the robot (overwrite first box if there is one)
        position = position.move(move.value)
        board[position.i][position.j] = MapItem.ROBOT

        # print("-----------Moved " + move.as_str() + "---------------")
        # print_board(board)

    print(get_gps_score(board))

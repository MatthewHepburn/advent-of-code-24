from typing import List, Dict

from common import get_adjacent_region_points
from loader import input_as_chars_trimmed
from grid import points_in_grid, GridPoint, Direction, is_in_bounds


class Region:
    def __init__(self, points: List[GridPoint], sides: int):
        self.points = points
        self.sides = sides

class Fences:
    up = False
    down = False
    left = False
    right = False


def get_adjacent_non_region_points(board: List[List[str]], point: GridPoint, directions: List[Direction]):
    region_symbol = board[point.i][point.j]

    output = []
    for direction in directions:
        adjacent = point.move(direction.value)
        if not is_in_bounds(board, adjacent) or board[adjacent.i][adjacent.j] != region_symbol:
            output.append(adjacent)

    return output

def get_sides(board: List[List[str]], points: List[GridPoint]) -> int:
    side_board = list()
    for line in board:
        side_board.append([Fences() for _ in range(0, len(line) + 2)])

    side_board.append([Fences() for _ in range(0, len(board[0]) + 2)])
    side_board.append([Fences() for _ in range(0, len(board[0]) + 2)])

    side_board_points = []
    for point in points:
        # These require a fence
        adjacent_points = get_adjacent_non_region_points(board, point, [Direction.LEFT])
        for adjacent in adjacent_points:
            side_board_point = GridPoint(adjacent.i + 1, adjacent.j + 1)
            side_board_points.append(side_board_point)
            side_board[side_board_point.i][side_board_point.j].right = True

        adjacent_points = get_adjacent_non_region_points(board, point, [Direction.RIGHT])
        for adjacent in adjacent_points:
            side_board_point = GridPoint(adjacent.i + 1, adjacent.j + 1)
            side_board_points.append(side_board_point)
            side_board[side_board_point.i][side_board_point.j].left = True

        adjacent_points = get_adjacent_non_region_points(board, point, [Direction.UP])
        for adjacent in adjacent_points:
            side_board_point = GridPoint(adjacent.i + 1, adjacent.j + 1)
            side_board_points.append(side_board_point)
            side_board[side_board_point.i][side_board_point.j].down = True

        adjacent_points = get_adjacent_non_region_points(board, point, [Direction.DOWN])
        for adjacent in adjacent_points:
            side_board_point = GridPoint(adjacent.i + 1, adjacent.j + 1)
            side_board_points.append(side_board_point)
            side_board[side_board_point.i][side_board_point.j].up = True

    # Look for vertical lines
    verts = 0
    for j in range(0, len(side_board[0])):
        left_in_line = False
        right_in_line = False
        for i in range(0, len(side_board)):
            fences = side_board[i][j]
            if left_in_line and not fences.left:
                left_in_line = False
            elif not left_in_line and fences.left:
                verts += 1
                left_in_line = True
            
            if right_in_line and not fences.right:
                right_in_line = False
            elif not right_in_line and fences.right:
                verts += 1
                right_in_line = True
            
            # print("Symbol = " + symbol, " next_is_line = ", next_is_line, " verts = ", verts)
    # print("Found ", verts, " vertical lines")

    # Look for horizontal lines
    horz = 0
    for side_line in side_board:
        up_in_line = False
        down_in_line = False
        for fences in side_line:
            if up_in_line and not fences.up:
                up_in_line = False
            elif not up_in_line and fences.up:
                horz += 1
                up_in_line = True

            if down_in_line and not fences.down:
                down_in_line = False
            elif not down_in_line and fences.down:
                horz += 1
                down_in_line = True

    # print("Found ", horz, " horizontal lines")

    return verts + horz

def get_points_in_region(board: List[List[str]], point: GridPoint) -> Region:
    points: Dict[str,GridPoint] = dict()
    region_symbol = board[point.i][point.j]

    frontier = [point]
    while len(frontier) > 0:
        new_frontier = []
        for point in frontier:
            points[point.as_str()] = point
            adjacent_points = get_adjacent_region_points(board, point)
            for adjacent_point in adjacent_points:
                if adjacent_point.as_str() in points:
                    continue
                points[adjacent_point.as_str()] = adjacent_point
                new_frontier.append(adjacent_point)

        frontier = new_frontier

    points: List[GridPoint] = list(points.values())
    sides = get_sides(board, points)

    return Region(points, sides)

if __name__ == "__main__":
    board = input_as_chars_trimmed()

    seen = dict()

    total = 0

    for point in points_in_grid(board):
        if point.as_str() in seen:
            continue

        region = get_points_in_region(board, point)
        region_symbol = board[point.i][point.j]
        sides = region.sides
        area = len(region.points)

        # print("A region of " + region_symbol + " plants with price ", area, " * ", sides, " = ", area * sides)

        total = total + (sides * area)
        for region_point in region.points:
            seen[region_point.as_str()] = point

    print(total)
from typing import List, Dict

from common import get_adjacent_region_points
from loader import input_as_chars_trimmed
from grid import points_in_grid, GridPoint, get_directly_adjacent

class Region:
    def __init__(self, points: List[GridPoint], perimeter: int):
        self.points = points
        self.perimeter = perimeter


def get_points_in_region(board: List[List[str]], point: GridPoint) -> Region:
    points: Dict[str, GridPoint] = dict()
    region_symbol = board[point.i][point.j]

    frontier = [point]
    perimeter = 0
    # if region_symbol == "B":
        # print("  Initial perimeter = " + str(perimeter))

    while len(frontier) > 0:
        # print("Frontier = ", [x.as_str() for x in frontier])
        new_frontier = []
        for point in frontier:
            points[point.as_str()] = point
            adjacent_points = get_adjacent_region_points(board, point)

            perimeter = perimeter + 4 - len(adjacent_points)
            # print("  Adding " + str(4 - len(adjacent_points)) + " to perimeter, to get " + str(perimeter))
            for adjacent_point in adjacent_points:
                if adjacent_point.as_str() in points:
                    continue
                points[adjacent_point.as_str()] = adjacent_point
                new_frontier.append(adjacent_point)

        frontier = new_frontier

    return Region(list(points.values()), perimeter)

if __name__ == "__main__":
    board = input_as_chars_trimmed()

    seen = dict()

    total = 0

    for point in points_in_grid(board):
        if point.as_str() in seen:
            continue

        region = get_points_in_region(board, point)
        region_symbol = board[point.i][point.j]
        perimeter = region.perimeter
        area = len(region.points)

        # print("A region of " + region_symbol + " plants with price ", area, " * ", perimeter, " = ", area * perimeter)

        total = total + (perimeter * area)
        for region_point in region.points:
            seen[region_point.as_str()] = point

    print(total)
from typing import Union, List

from loader import input_as_chars_trimmed
from grid import points_in_grid, GridPoint, get_directly_adjacent, print_points_on_grid


class Trailhead:
    height = 0

    def __init__(self):
        self.peaks = set()

class Ground:
    def __init__(self, height: int):
        self.height = height


def find_paths(map: List[List[Union[Trailhead, Ground]]], point: GridPoint):
    frontier = [point]

    for _ in range(0, 9):
        new_frontier = []
        for path_point in frontier:
            point_height = map[path_point.i][path_point.j].height
            for adjacent in get_directly_adjacent(map, path_point):
                adjacent_area = map[adjacent.i][adjacent.j]
                if adjacent_area.height == point_height + 1:
                    new_frontier.append(adjacent)
        frontier = new_frontier

    return frontier


if __name__ == "__main__":
    input = input_as_chars_trimmed()

    map: List[List[Union[Trailhead, Ground]]] = []
    for line in input:
        map.append([Ground(int(x)) if int(x) > 0 else Trailhead() for x in line])

    total = 0
    for point in points_in_grid(map):
        if map[point.i][point.j].height != 0:
            continue

        trailhead = map[point.i][point.j]
        # print("Considering trailhead at " + point.as_str())
        paths = find_paths(map, point)
        # print("Found " + str(len(paths)) + " paths", paths)
        total = total + len(paths)

    print(total)
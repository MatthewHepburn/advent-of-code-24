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


def find_peaks(trailhead: Trailhead, map: List[List[Union[Trailhead, Ground]]], point: GridPoint):
    frontier = [point]
    visited = set()

    while len(frontier) > 0:
        # print_points_on_grid(map, frontier)
        new_frontier = []
        for point in frontier:
            point_height = map[point.i][point.j].height
            for adjacent in get_directly_adjacent(map, point):
                adjacent_area = map[adjacent.i][adjacent.j]
                if adjacent.as_str() in visited:
                    continue
                if adjacent_area.height == point_height + 1:
                    if adjacent_area.height == 9:
                        trailhead.peaks.add(adjacent.as_str())
                    else:
                        new_frontier.append(adjacent)

            visited.add(point.as_str())

        frontier = new_frontier

    return trailhead.peaks


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
        peaks = find_peaks(trailhead, map, point)
        # print("Found " + str(len(peaks)) + " peaks", peaks)
        total = total + len(peaks)

    print(total)
import os
import re
from typing import List, Optional

from grid import GridPoint, GridVector
from loader import input_as_strings

# This isn't really a solution, just a way to narrow down the line noise enough to be able to visually filter it

class Guard:
    def __init__(self, position: GridPoint, vector: GridVector):
        self.position = position
        self.vector = vector

    def as_str(self) -> str:
        return f'p={self.position.i},{self.position.j} v={self.vector.i},{self.vector.j}'


def print_state(guards: List[Guard], width: int, height: int):
    print("---------------------")
    for j in range(0, height):
        line = ''
        for i in range(0, width):
            guards_here = [x for x in guards if x.position.i == i and x.position.j == j]
            symbol = "." if guards_here == [] else str(len(guards_here))
            line = line + symbol
        print(line)


def get_quadrant(point: GridPoint, width: int, height: int) -> Optional[int]:
    width_midpoint = width // 2
    height_midpoint = height // 2

    if point.j < height_midpoint and point.i < width_midpoint:
        return 0
    elif point.j < height_midpoint and point.i > width_midpoint:
        return 1
    elif point.j > height_midpoint and point.i < width_midpoint:
        return 2
    elif point.j > height_midpoint and point.i > width_midpoint:
        return 3

    return None


def is_tree_candidate(guards: List[Guard], width: int, height: int)-> bool:
    # Surely a tree should have the top corners free(ish
    bad = 0
    for guard in guards:
        if guard.position.j < 5 and guard.position.i < 20:
            bad = bad + 1
        elif guard.position.j < 5 and guard.position.i > 80:
            bad = bad + 1
        elif guard.position.j < 10 and guard.position.i < 10:
            bad = bad + 1
        elif guard.position.j < 10 and guard.position.i > 90:
            bad = bad + 1

    return bad < 3

    # Surely a tree would have a point in the top middle(ish)?
    # points = [GridPoint(width//2, 0), GridPoint(1 + width // 2, 0), GridPoint(-1 + width // 2, 0)]
    # found = False
    # for point in points:
    #     if found:
    #         break
    #     for guard in guards:
    #         if guard.position.i == point.i and guard.position.j == point.j:
    #             found = True
    #             break
    #
    # return found
    # if not found:
    #     return False

    # Test for approximate symetry? E.g. x% of rows must be symmetric?
    # Left total must be close to right total
    width_midpoints = width // 2
    # rightness_by_line = dict()
    # for guard in guards:
    #     rightness = guard.position.i
    #     line = guard.position.j
    #     this_list = rightness_by_line[line] if line in rightness_by_line else []
    #     this_list.append(rightness)
    #     rightness_by_line[line] = this_list
    #
    # even_lines = 0
    # for line, rightnesses in rightness_by_line.items():
    #     if len(set(rightnesses)) % 2 == 0:
    #         even_lines = even_lines +1
    #
    # return even_lines > 65
    #
    # midpoints = []
    # for line, rightnesses in rightness_by_line.items():
    #     uniq_rightnesses = set(rightnesses)
    #     midpoints.append(sum(uniq_rightnesses) / len(uniq_rightnesses))
    #
    # avg_midpoint = sum(midpoints) / len(midpoints)
    # deviation = 0
    # for midpoint in midpoints:
    #     deviation += abs(midpoint - avg_midpoint)
    #
    # avg_deviation = deviation / len(midpoints)
    #
    # return avg_deviation < 8
    #
    # midpoint_freq = dict()
    # for midpoint in midpoints:
    #     intmidpoint = int(midpoint)
    #     midpoint_freq[intmidpoint] = 1 if intmidpoint not in midpoint_freq else midpoint_freq[intmidpoint] + 1
    #
    # most_frequent = None
    # most_frequent_freq = None
    # for midpoint, freq in midpoint_freq.items():
    #     most_frequent = midpoint if most_frequent_freq is None or freq > most_frequent_freq else most_frequent
    #     most_frequent_freq = freq if most_frequent_freq is None or freq > most_frequent_freq else most_frequent_freq
    #
    # aligned = 0
    # for midpoint in midpoints:
    #     if abs(int(midpoint) - most_frequent) < 2:
    #         aligned = aligned + 1
    #
    # if aligned > 19:
    #     print(f"{aligned} aligned on midpoint = {most_frequent}")
    # return aligned > 20

def hash_position(guards:List[Guard]) -> int:
    strs = [x.position.as_str() for x in guards]
    pos_str = "".join(strs)
    return hash(pos_str)

if __name__ == "__main__":
    input = input_as_strings()

    guards = []

    for line in input:
        values = [int(x) for x in re.findall("-?[0-9]+", line)]
        position = GridPoint(values[0], values[1])
        vector = GridVector(values[2], values[3])
        guards.append(Guard(position, vector))

    is_example = os.getenv('AOC_EXAMPLE_MODE') == "1"

    width = 11 if is_example else 101
    height = 7 if is_example else 103

    quadrants = [[], [], [], []]

    # print_state(guards, width, height)
    seen_positions = dict()

    # Repeats after 10404
    for i in range(1, 10404):
        for guard in guards:
            raw_pos = guard.position.move(guard.vector)
            wrapped_pos = GridPoint(raw_pos.i % width, raw_pos.j % height)
            guard.position = wrapped_pos
        # position_hash = hash_position(guards)
        # if position_hash in seen_positions:
        #     print("Repeated Position! i = " + str(i))
        #     break
        # seen_positions[position_hash] = True
        if i % 10000 == 0:
            print(f"{i} seconds elapsed")
        if is_tree_candidate(guards, width, height):
            print_state(guards, width, height)
            print(f"{i} seconds elapsed")
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
    # Having found the tree by staring at a lot of line noise, I was able to identify properties allowing a computer to find the solution

    rightness_by_line = dict()
    for guard in guards:
        rightness = guard.position.i
        line = guard.position.j
        this_list = rightness_by_line[line] if line in rightness_by_line else []
        this_list.append(rightness)
        rightness_by_line[line] = this_list

    # How many lines have long runs of adjacent guards?
    lines_with_rows = 0
    for line, rightnesses in rightness_by_line.items():
        rightnesses.sort()
        run_length = 0
        last = 0
        for rightness in rightnesses:
            if rightness - last == 1:
                run_length = run_length + 1
            else:
                if run_length > 5:
                    lines_with_rows = lines_with_rows + 1
                    break
                run_length = 0
            last = rightness

    return lines_with_rows > 5


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

    # Repeats after 10404
    for i in range(1, 10404):
        for guard in guards:
            raw_pos = guard.position.move(guard.vector)
            wrapped_pos = GridPoint(raw_pos.i % width, raw_pos.j % height)
            guard.position = wrapped_pos

        if is_tree_candidate(guards, width, height):
            print_state(guards, width, height)
            print(i)
            break
import os
import re
from typing import List, Optional

from grid import GridPoint, GridVector
from loader import input_as_strings

class Guard:
    def __init__(self, position: GridPoint, vector: GridVector):
        self.position = position
        self.vector = vector

    def as_str(self)-> str:
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

def print_state_with_quads(guards: List[Guard], width: int, height: int):
    print("---------------------")
    for j in range(0, height):
        line = ''
        for i in range(0, width):
            guards_here = [x for x in guards if x.position.i == i and x.position.j == j]
            symbol = "." if guards_here == [] else str(len(guards_here))
            if get_quadrant(GridPoint(i, j), width, height) is None:
                symbol = " "
            line = line + symbol
        print(line)

if __name__ == "__main__":
    input = input_as_strings()

    guards = []

    for line in input:
        values = [int(x) for x in re.findall("-?[0-9]+", line)]
        position = GridPoint(values[0], values[1])
        vector = GridVector(values[2], values[3])
        guards.append(Guard(position, vector))

    print("Loaded " + str(len(guards)) + " guards")
    is_example = os.getenv('AOC_EXAMPLE_MODE') == "1"

    # These got a bit mixed up as to which is width, which is height
    width = 11 if is_example else 101
    height = 7 if is_example else 103

    quadrants = [[], [], [], []]

    # print_state(guards, width, height)

    for guard in guards:
        for _ in  range(0, 100):
            vec = guard.vector
            raw_pos = guard.position.move(vec)
            wrapped_pos = GridPoint(raw_pos.i % width, raw_pos.j % height)
            guard.position = wrapped_pos

    print_state_with_quads(guards, width, height)

    quadrants = [[], [], [], []]
    for guard in guards:
        quadrant = get_quadrant(guard.position, width, height)
        if quadrant is not None:
            quadrants[quadrant].append(guard.position)
        

    safety_factor = 1
    factors = [len(q) for q in quadrants]
    # print(quadrants)
    for quadrant in quadrants:
        safety_factor = safety_factor * len(quadrant)

    print(f"Safety factor = {factors[0]} * {factors[1]} * {factors[2]} * {factors[3]}")

    print(safety_factor)
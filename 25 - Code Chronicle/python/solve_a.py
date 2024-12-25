from typing import List, Union

from common import EmptyPosition, WallPosition, get_start_position, get_end_position
from grid import GridPoint, is_in_bounds, get_directly_adjacent, points_in_grid, GridVector
from loader import input_as_chars_trimmed, input_as_strings


def process_input(lines: List[str]) -> (bool, List[int]):
    is_lock = '.' not in lines[0]

    values = [10 for _ in range(0, len(lines[0]))]

    symbol = '.' if is_lock else '#'
    for i in range(0, len(lines)):
        line = lines[i]
        for j in range(0, len(line)):
            if line[j] == symbol:
                values[j] = min(i -1, values[j])

    # invert values for keys, since we measure from the bottom
    if not is_lock:
        values = [len(lines) -2 - v for v in values]

    return is_lock, values


def fits(lock: List[int], key: List[int]):
    for i in range(0, len(lock)):
        if key[i] + lock[i] > 5:
            return False

    return True


if __name__ == "__main__":
    input = [l.strip() for l in input_as_strings()]

    keys = []
    locks = []

    current = []
    for line in input:
        if line == '':
            is_lock, values = process_input(current)
            if is_lock:
                locks.append(values)
            else:
                keys.append(values)
            current = []
        else:
            current.append(line)

    is_lock, values = process_input(current)
    if is_lock:
        locks.append(values)
    else:
        keys.append(values)
    current = []

    # for l in locks:
    #     print("LOCK: ", l)
    #
    # for k in keys:
    #     print("KEY: ", k)

    valid_pairs = 0
    for l in locks:
        for k in keys:
            if fits(l, k):
                valid_pairs = valid_pairs + 1
                # print("Match - l =", l, " k = ", k)

    print(valid_pairs)

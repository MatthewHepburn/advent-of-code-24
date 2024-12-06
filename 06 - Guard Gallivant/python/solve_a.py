from typing import List, Optional

from grid import GridPoint, Direction, is_in_bounds
from loader import input_as_chars

def position_of(grid: List[List[str]], needles: List[str]) -> Optional[GridPoint]:
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] in needles:
                return GridPoint(i, j)
    return None

if __name__ == "__main__":
    board = input_as_chars()

    visited: List[List[bool]] = []
    for i in range(0, len(board)):
        line = []
        for j in range(0, len(board[i])):
            line.append(False)
        visited.append(line)

    guard_position = position_of(board, ['^'])
    if guard_position is None:
        raise Exception("No start pos")

    visited[guard_position.i][guard_position.j] = True
    direction: Direction = Direction.UP

    in_bounds = True
    while in_bounds:
        next_pos = guard_position.move(direction.value)
        next_pos_value = None
        next_pos_inbounds = is_in_bounds(board, next_pos)
        if next_pos_inbounds:
            next_pos_value = board[next_pos.i][next_pos.j]
        if  next_pos_value == '#':
            # Unable to go this way, rotate:
            direction = direction.rotate_clockwise()
            continue

        guard_position = next_pos
        in_bounds = next_pos_inbounds
        if in_bounds:
            visited[guard_position.i][guard_position.j] = True

    visted_total = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if visited[i][j]:
                visted_total = visted_total + 1

    print(visted_total)
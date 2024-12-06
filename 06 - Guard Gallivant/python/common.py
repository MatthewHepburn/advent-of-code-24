from typing import List, Optional

from grid import Direction, GridPoint, is_in_bounds

def position_of(grid: List[List[str]], needles: List[str]) -> Optional[GridPoint]:
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] in needles:
                return GridPoint(i, j)
    return None

def get_visted_if_terminates(board: List[List[str]], start: GridPoint) -> Optional[List[List[List[Direction]]]]:
    guard_position = start
    direction: Direction = Direction.UP

    # Record every direction we've gone in for each point, to allow detecting loops
    visited: List[List[List[Direction]]] = []
    for i in range(0, len(board)):
        line = []
        for j in range(0, len(board[i])):
            line.append([])
        visited.append(line)

    visited[guard_position.i][guard_position.j].append(direction)

    in_bounds = True
    while in_bounds:
        next_pos = guard_position.move(direction.value)
        next_pos_value = None
        next_pos_inbounds = is_in_bounds(board, next_pos)
        if next_pos_inbounds:
            next_pos_value = board[next_pos.i][next_pos.j]
        if next_pos_value == '#':
            # Unable to go this way, rotate:
            direction = direction.rotate_clockwise()
            continue

        guard_position = next_pos
        in_bounds = next_pos_inbounds
        if in_bounds:
            if direction in visited[guard_position.i][guard_position.j]:
                # In a loop!
                return None
            visited[guard_position.i][guard_position.j].append(direction)

    return visited
from typing import List, Optional

from common import get_visted_if_terminates
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

    guard_position = position_of(board, ['^'])
    if guard_position is None:
        raise Exception("No start pos")

    visited = get_visted_if_terminates(board, guard_position)

    visited_total = 0
    for i in range(0, len(visited)):
        for j in range(0, len(visited[i])):
            if len(visited[i][j]) > 0:
                visited_total = visited_total + 1

    print(visited_total)
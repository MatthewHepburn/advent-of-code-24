from typing import List, Dict

from common import get_transmitter_map
from grid import GridPoint, points_in_grid, is_in_bounds
from loader import input_as_chars_trimmed

def get_antinodes(a: GridPoint, b: GridPoint) -> List[GridPoint]:
    a_to_b = a.vector_to(b)
    b_to_a = b.vector_to(a)

    return [b.move(a_to_b), a.move(b_to_a)]


if __name__ == "__main__":
    board = input_as_chars_trimmed()

    antinodes_grid = []
    for i in range(0, len(board)):
        row = []
        for j in range(0, len(board[i])):
            row.append(False)
        antinodes_grid.append(row)

    transmitter_map = get_transmitter_map(board)

    for type, points in transmitter_map.items():
        for i in range(0, len(points)):
            point_a = points[i]
            for j in range(i + 1, len(points)):
                point_b = points[j]
                antinodes = get_antinodes(point_a, point_b)
                for antinode in antinodes:
                    if is_in_bounds(antinodes_grid, antinode):
                        antinodes_grid[antinode.i][antinode.j] = True

    total = 0
    for point in points_in_grid(antinodes_grid):
        if antinodes_grid[point.i][point.j]:
            total = total + 1

    print(total)

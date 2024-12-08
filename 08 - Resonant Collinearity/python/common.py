from typing import List, Dict

from grid import points_in_grid, GridPoint

def get_transmitter_map(board: List[List[str]]) -> Dict[str, List[GridPoint]]:
    map = dict()
    for point in points_in_grid(board):
        value = board[point.i][point.j]
        if value == '.':
            continue
        if not value in map:
            map[value] = []
        map[value].append(point)

    return map
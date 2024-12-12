from typing import List

from grid import GridPoint, get_directly_adjacent

def get_adjacent_region_points(board: List[List[str]], point: GridPoint):
    region_symbol = board[point.i][point.j]
    return [adj_point for adj_point in get_directly_adjacent(board, point) if board[adj_point.i][adj_point.j] == region_symbol]
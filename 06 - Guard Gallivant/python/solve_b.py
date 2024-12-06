import copy

from common import get_visted_if_terminates, position_of
from grid import GridPoint
from loader import input_as_chars

if __name__ == "__main__":
    board = input_as_chars()

    start_position = position_of(board, ['^'])
    if start_position is None:
        raise Exception("No start pos")

    visited = get_visted_if_terminates(board, start_position)

    # Only worth putting an obstacle somewhere we know the guard will walk
    candidate_positions = []
    for i in range(0, len(visited)):
        for j in range(0, len(visited[i])):
            if len(visited[i][j]) > 0 and not (i == start_position.i and j == start_position.j):
                candidate_positions.append(GridPoint(i, j))

    loop_options = 0
    for candidate_position in candidate_positions:
        possible_board = copy.deepcopy(board)
        possible_board[candidate_position.i][candidate_position.j] = '#'

        visited_or_none = get_visted_if_terminates(possible_board, start_position)
        if visited_or_none is None:
            print(candidate_position.i, candidate_position.j)
            loop_options = loop_options + 1


    print(loop_options)
import copy
from typing import List

from common import get_visted_if_terminates, position_of
from grid import GridPoint, Direction
from loader import input_as_chars

class ObstructionCandidate:
    def __init__(self, position: GridPoint, first_visit_direction: Direction):
        self.position = position
        self.first_visit_direction = first_visit_direction

if __name__ == "__main__":
    board = input_as_chars()

    start_position = position_of(board, ['^'])
    if start_position is None:
        raise Exception("No start pos")

    visited = get_visted_if_terminates(board, start_position, Direction.UP)

    # Only worth putting an obstacle somewhere we know the guard will walk
    obstruction_candidates: List[ObstructionCandidate] = []
    for i in range(0, len(visited)):
        for j in range(0, len(visited[i])):
            if len(visited[i][j]) > 0 and not (i == start_position.i and j == start_position.j):
                candidate = ObstructionCandidate(GridPoint(i, j), visited[i][j][0])
                obstruction_candidates.append(candidate)

    loop_options = 0
    for obstruction_candidate in obstruction_candidates:
        possible_board = copy.deepcopy(board)
        possible_board[obstruction_candidate.position.i][obstruction_candidate.position.j] = '#'

        # Rather than playing all the way through from the start position, start from 1 step before
        # the obstruction square is first visited
        back = obstruction_candidate.first_visit_direction.rotate_clockwise().rotate_clockwise()
        search_start_position = obstruction_candidate.position.move(back.value)

        visited_or_none = get_visted_if_terminates(possible_board, search_start_position, obstruction_candidate.first_visit_direction)
        if visited_or_none is None:
            print(obstruction_candidate.position.i, obstruction_candidate.position.j)
            loop_options = loop_options + 1


    print(loop_options)
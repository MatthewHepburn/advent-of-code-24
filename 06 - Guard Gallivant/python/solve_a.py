from common import get_visted_if_terminates, position_of
from grid import Direction
from loader import input_as_chars

if __name__ == "__main__":
    board = input_as_chars()

    guard_position = position_of(board, ['^'])
    if guard_position is None:
        raise Exception("No start pos")

    visited = get_visted_if_terminates(board, guard_position, Direction.UP)

    visited_total = 0
    for i in range(0, len(visited)):
        for j in range(0, len(visited[i])):
            if len(visited[i][j]) > 0:
                visited_total = visited_total + 1

    print(visited_total)
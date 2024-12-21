import os
import re

from common import EmptyPosition, CorruptedPosition, BoardType, get_best_route_length
from grid import GridPoint
from loader import input_as_strings

if __name__ == "__main__":
    input = input_as_strings()

    is_example = os.getenv('AOC_EXAMPLE_MODE') == "1"
    grid_size = 7 if is_example else 71

    last_byte = None

    bytes_to_read = 12 if is_example else 1024
    while True:
        # print(f"bytes_to_read = {bytes_to_read}")
        board: BoardType = []
        for _ in range(0, grid_size):
            line = []
            for _ in range(0, grid_size):
                line.append(EmptyPosition())
            board.append(line)


        for b in range(0, bytes_to_read):
            byte_line = input[b]
            coords = [int(x) for x in re.findall('[0-9]+', byte_line)]
            corrupt_point = GridPoint(coords[0], coords[1])
            board[corrupt_point.i][corrupt_point.j] = CorruptedPosition()
            last_byte = f"{corrupt_point.i},{corrupt_point.j}"

        score = get_best_route_length(board)
        if score is None:
            break
        bytes_to_read = bytes_to_read + 1

    print(last_byte)
from typing import List, Optional

from grid import GridPoint, direction_from_str, points_in_grid, Direction
from loader import input_as_strings


class Keypad:
    def __init__(self, keys: List[List[str]]):
        for point in points_in_grid(keys):
            if keys[point.i][point.j] == 'A':
                self.start_position = point

        self.keys = keys
        assert self.keys[self.start_position.i][self.start_position.j] == 'A'

    def is_safe(self, position:GridPoint) -> bool:
        return self.keys[position.i][position.j] != ''

    def get_directions_to(self, position: GridPoint, char: str) -> List[str]:
        target = None
        for point in points_in_grid(self.keys):
            if self.keys[point.i][point.j] == char:
                target = point
                break

        assert target is not None

        output = []

        i_diff = target.i - position.i
        if i_diff < 0 and self.is_safe(position.move(Direction.UP.value)):
            output.append('^')
        elif i_diff > 0 and self.is_safe(position.move(Direction.DOWN.value)):
            output.append('v')

        j_diff = target.j - position.j
        if j_diff < 0 and self.is_safe(position.move(Direction.LEFT.value)):
            output.append('<')
        elif j_diff > 0 and self.is_safe(position.move(Direction.RIGHT.value)):
            output.append('>')

        if not output:
            # No change in position needed, so push required
            output.append('A')

        # print(f"From {position.as_str()} to {target.as_str()} = ", output)
        return output

    def send_instruction(self, position: GridPoint, inst: str) -> (GridPoint, Optional[str]):
        if inst == 'A':
            return position, self.keys[position.i][position.j]

        direction = direction_from_str(inst)
        position = position.move(direction.value)
        if self.keys[position.i][position.j] == '':
            raise Exception("PANIC: moved to empty space on input device")

        return position, None


    def get_best_sequences(self, code: str):
        start_pos = self.start_position
        sequences = []

        frontier = [(start_pos, code, [])]
        while frontier:
            new_frontier = []

            for position, code, moves in frontier:
                for move in self.get_directions_to(position, code[0]):
                    new_position, push = self.send_instruction(position, move)
                    new_code = code
                    my_moves = moves[:]
                    my_moves.append(move)

                    if push is not None:
                        assert push == code[0]
                        new_code = code[1:]

                    if len(new_code) > 0:
                        new_frontier.append((new_position, new_code, my_moves))
                    else:
                        sequences.append(my_moves)

            frontier = new_frontier

        # best_sequence_length = min([len(s) for s in sequences])
        # return [s for s in sequences if len(s) < best_sequence_length + 12]
        return sequences


if __name__ == "__main__":
    input = [x.strip() for x in input_as_strings()]

    # Did the layout change? I didn't make this ASCII art but it doesn't match the question any more...
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    # | 0 | A |
    # +---+---+
    numpad_keys = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['', '0', 'A']
    ]

    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    dpad_keys = [
        ['', '^', 'A'],
        ['<', 'v', '>']
    ]

    # Work out the shortest way to enter each sequence on the first dpad up the stack
    # We need to account for possible states in the top dpad - others in stack will always start/end on A, but that may not
    seqs = dict()
    numpad1 = Keypad(dpad_keys)
    numpad2 = Keypad(dpad_keys)
    for start_point in points_in_grid(dpad_keys):
        if dpad_keys[start_point.i][start_point.j] == '':
            continue

        for target in ["<", ">", "^", "v", "A"]:
            numpad1.start_position = start_point
            numpad1_sequences = numpad1.get_best_sequences(target)
            nice = ["".join(s) for s in numpad1_sequences]
            print(f'Best numpad_1 seqs for {target} = ', nice)

            numpad2_sequences = []
            for numpad1_sequence in numpad1_sequences:
                sequences = numpad2.get_best_sequences("".join(numpad1_sequence))
                numpad2_sequences = numpad2_sequences + sequences

            nice = ["".join(s) for s in numpad2_sequences]
            # print(f'Best numpad 2 seqs for {target} = ', nice)

            end_pos = None
            for point in points_in_grid(dpad_keys):
                if dpad_keys[point.i][point.j] == target[-1]:
                    end_pos = point
                    break

            assert end_pos is not None

            key = start_point.as_str() + " -> " + target

            shortest_len = min([len(s) for s in numpad2_sequences])
            shortest_seq = ["".join(s) for s in numpad2_sequences if len(s) == shortest_len][0]
            seqs[key] = (shortest_seq, end_pos)

    print(seqs)

    total = 0
    for code in input:
        keypad = Keypad(numpad_keys)
        numpad1 = Keypad(dpad_keys)
        numpad2 = Keypad(dpad_keys)
        numpad3 = Keypad(dpad_keys)

        keypad_sequences = keypad.get_best_sequences(code)

        print(f"Keypad sequences for {code} = ", ["".join(s) for s in keypad_sequences])

        best = None
        best_seq = None
        for seq in keypad_sequences:
            input_seq = ''
            dpad_pos = GridPoint(0,2)
            for char in seq:
                key = dpad_pos.as_str() + " -> " + char
                this_seq, dpad_pos = seqs[key]
                input_seq = input_seq + this_seq

            seq_len = len(input_seq)
            best = seq_len if best is None or seq_len < best else best
            if best == seq_len:
                best_seq = input_seq


        print(best_seq)

        numeric_value = int(code.replace('A', ''))
        print(f"Score for {code} = {best} x {numeric_value} = {best * numeric_value}")
        total = total + (best * numeric_value)

    print(total)





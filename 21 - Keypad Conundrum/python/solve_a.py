from typing import List, Union, Optional

from common import EmptyPosition, WallPosition, get_start_position, get_end_position
from grid import GridPoint, direction_from_str, points_in_grid, GridVector
from loader import input_as_chars_trimmed, input_as_strings

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
class Keypad:
    keys = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['', '0', 'A']
    ]

    def __init__(self):
        self.position = GridPoint(3,2)
        assert self.keys[self.position.i][self.position.j] == 'A'

    def get_directions_to(self, char: str) -> List[str]:
        target = None
        for point in points_in_grid(self.keys):
            if self.keys[point.i][point.j] == char:
                target = point
                break

        assert target is not None

        output = []
        i_diff = target.i - self.position.i
        if i_diff < 0:
            output.append('^')
        elif i_diff > 0:
            output.append('v')

        j_diff = target.j - self.position.j
        if j_diff < 0:
            output.append('<')
        elif j_diff > 0:
            output.append('>')

        if not output:
            # No change in position needed, so push required
            output.append('A')

        return output

    def send_instruction(self, inst: str) -> Optional[str]:
        if inst == 'A':
            return self.keys[self.position.i][self.position.j]

        direction = direction_from_str(inst)
        self.position = self.position.move(direction.value)
        if self.keys[self.position.i][self.position.j] == '':
            raise Exception("PANIC: moved to empty space on input device")


    def get_best_sequences(self, code: str):
        start_pos = self.position
        sequences = []


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
class Numpad:
    keys = [
        ['', '^', 'A'],
        ['<', 'v', '>']
    ]

    def __init__(self, subject: Union[Keypad, 'Numpad']):
        self.position = GridPoint(0,2)
        assert self.keys[self.position.i][self.position.j] == 'A'

        self.subject = subject
        subject.controlled_by = self


if __name__ == "__main__":
    input = [x.strip() for x in input_as_strings()]

    for code in input:
        keypad = Keypad()
        numpad1 = Numpad(keypad)
        numpad2 = Numpad(numpad1)
        numpad3 = Numpad(numpad2)

        keypad_sequences = keypad.get_best_sequences(code)





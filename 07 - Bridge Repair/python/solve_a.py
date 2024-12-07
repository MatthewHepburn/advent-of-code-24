import copy
from typing import List

from loader import input_as_strings

class Equation:
    def __init__(self, result: int, value_list: List[int]):
        self.result : int = result
        self.value_list : List[int] = value_list
        assert len(value_list) > 1

    def __str__(self):
        return str(self.result) + ": " + " ".join([str(x) for x in self.value_list])

    def get_operator_positions(self) -> List[int]:
        return list(range(1, len(self.value_list)))

    def evaluate(self, functions: List[callable]):
        value = self.value_list[0]
        for i in range(1, len(self.value_list)):
            function = functions[i - 1]
            prev_val = value
            value = function(value, self.value_list[i])

        return value

    def from_string(input: str):
        [result_str, values_str] = input.split(': ')
        result = int(result_str)
        values = [int(x) for x in values_str.split(" ")]
        return Equation(result, values)

def plus(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b

def permuations_with_repetition_fixed_len(values, length: int):
    assert len(values) > 0
    value_indices = [i for i in range(0, length)]
    previous = [0 for _ in range(0, length)]

    placeholder_output = [copy.copy(previous)]
    while True:
        next = []
        rollover = True
        for i in range(0, length):
            cur_val_index = previous[i]
            if rollover:
                new_index = (cur_val_index + 1) % len(values)
                rollover = new_index == 0
            else:
                new_index = cur_val_index
            next.append(new_index)

        placeholder_output.append(next)
        previous = next

        if rollover:
            break

    output = []
    for placeholder in placeholder_output:
        output.append([values[i] for i in placeholder])

    return output

if __name__ == "__main__":
    input = input_as_strings()
    equations = [Equation.from_string(line) for line in input]

    total = 0
    operators = [plus, multiply]
    for equation in equations:
        for functions in permuations_with_repetition_fixed_len(operators, len(equation.get_operator_positions())):
            result = equation.evaluate(functions)
            if result == equation.result:
                total = total + result
                break

    print(total)


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

    def test(self, functions: List[callable]) -> bool:
        value = self.value_list[0]
        for i in range(1, len(self.value_list)):
            function = functions[i - 1]
            value = function(value, self.value_list[i])

            # Operators only increase our value, so we can short circuit if our number gets too large
            if value > self.result:
                return False

        return value == self.result

    def from_string(input: str):
        [result_str, values_str] = input.split(': ')
        result = int(result_str)
        values = [int(x) for x in values_str.split(" ")]
        return Equation(result, values)

def plus(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b

def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))

def permutations_with_repetition_fixed_len(values, length: int):
    assert len(values) > 0
    previous = [0 for _ in range(0, length)]

    yield [values[i] for i in previous]

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
        yield [values[i] for i in previous]

        if rollover:
            break

def solve(operators: List[callable]) -> int:
    input = input_as_strings()
    equations = [Equation.from_string(line) for line in input]

    total = 0
    for equation in equations:
        # To really speed this up, we need to feed back function sequence prefixes we have ruled out
        # due to them producing results too large int our permutation generator.
        # But that's more work than I want to do right now!
        for functions in permutations_with_repetition_fixed_len(operators, len(equation.get_operator_positions())):
            if equation.test(functions):
                total = total + equation.result
                break

    return total
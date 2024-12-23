import re
from typing import Tuple, List, Optional

from loader import input_as_strings


class MachineState:
    inst = 0
    reg_a = 0
    reg_b = 0
    reg_c = 0

    def as_str(self):
        return f"inst={self.inst}, A={self.reg_a}, B={self.reg_b}, C={self.reg_c}"


def get_instruction(opcode: int) -> str:
    if opcode == 0:
        return "adv"
    elif opcode == 1:
        return "bxl"
    elif opcode == 2:
        return "bst"
    elif opcode == 3:
        return "jnz"
    elif opcode == 4:
        return "bxc"
    elif opcode == 5:
        return "out"
    elif opcode == 6:
        return "bdv"
    elif opcode == 7:
        return "cdv"
    raise Exception("Unknown opcode " + str(opcode))


def read_combo_operand(state: MachineState, input: int) -> int:
    if input <= 3:
        return input
    if input == 4:
        return state.reg_a
    if input == 5:
        return state.reg_b
    if input == 6:
        return state.reg_c
    raise Exception("Unexpected operand: " + str(input))

def xor(a: int, b: int) -> int:
    return (a | b) & ~(a & b)

def step(state: MachineState, program: List[int])-> Optional[int]:
    instruction = get_instruction(program[state.inst])
    literal_operand = program[state.inst + 1]

    # print(f"Executing {instruction} with {literal_operand}")

    jumped = False
    output = None
    if instruction == "adv":
        before = state.reg_a
        operand = read_combo_operand(state, literal_operand)
        result = state.reg_a // (2 ** operand)
        state.reg_a = result
#         print(f"  A = {result} = {before} // 2 ^ {operand}")
    elif instruction == "bxl":
        before = state.reg_b
        result = xor(state.reg_b, literal_operand)
        state.reg_b = result
#         print(f"  B = {result} = xor({before}, {literal_operand})")
    elif instruction == "bst":
        operand = read_combo_operand(state, literal_operand)
        result = operand % 8

        state.reg_b = result
#         print(f"  B = {result} = {operand} % 8")
    elif instruction == "jnz":
        if state.reg_a != 0:
            state.inst = literal_operand
            jumped = True
    elif instruction == "bxc":
        before = state.reg_b
        result = xor(state.reg_b, state.reg_c)
        state.reg_b = result
#         print(f"  B = {result} = xor({before}, {state.reg_c})")
    elif instruction == "out":
        result = read_combo_operand(state, literal_operand) % 8
        output = result
    elif instruction == "bdv":
        result = state.reg_a // (2 ** read_combo_operand(state, literal_operand))
        state.reg_b = result
#         print(f"  B = {result}")
    elif instruction == "cdv":
        operand = read_combo_operand(state, literal_operand)
        result = state.reg_a // (2 ** operand)
        state.reg_c = result
#         print(f"  C = {result} = {state.reg_a} // (2 ^ {operand})")
    else:
        raise Exception("Unknown instruction: " + instruction)


    if not jumped:
        state.inst = state.inst + 2

    return output

def read_machine()-> Tuple[MachineState, List[int]]:
    input = input_as_strings()

    state = MachineState()
    program = []
    for line in input:
        if "Register A" in line:
            state.reg_a = int(re.findall('[0-9]+', line)[0])
        elif "Register B" in line:
            state.reg_b = int(re.findall('[0-9]+', line)[0])
        elif "Register C" in line:
            state.reg_c = int(re.findall('[0-9]+', line)[0])
        elif "Program" in line:
            program = [int(x) for x in re.findall('[0-9]+', line)]

    return state, program
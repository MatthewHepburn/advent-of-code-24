import re
from typing import List, Optional

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

# The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
# The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
# The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
# The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
# The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
# The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
# The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
# The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)


def step(state: MachineState, program: List[int])-> Optional[int]:
    instruction = get_instruction(program[state.inst])
    literal_operand = program[state.inst + 1]

    # print(f"Executing {instruction} with {literal_operand}")

    jumped = False
    output = None
    if instruction == "adv":
        result = state.reg_a // (2 ** read_combo_operand(state, literal_operand))
        state.reg_a = result
    elif instruction == "bxl":
        result = xor(state.reg_b, literal_operand)
        state.reg_b = result
    elif instruction == "bst":
        result = read_combo_operand(state, literal_operand) % 8
        state.reg_b = result
    elif instruction == "jnz":
        if state.reg_a != 0:
            state.inst = literal_operand
            jumped = True
    elif instruction == "bxc":
        result = xor(state.reg_b, state.reg_c)
        state.reg_b = result
    elif instruction == "out":
        result = read_combo_operand(state, literal_operand) % 8
        output = result
    elif instruction == "bdv":
        result = state.reg_a // (2 ** read_combo_operand(state, literal_operand))
        state.reg_b = result
    elif instruction == "cdv":
        result = state.reg_a // (2 ** read_combo_operand(state, literal_operand))
        state.reg_c = result
    else:
        raise Exception("Unknown instruction: " + instruction)


    if not jumped:
        state.inst = state.inst + 2

    return output


if __name__ == "__main__":
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

    # print(program)

    output = []
    while state.inst in range(0, len(program)):
        # print(state.as_str())

        this_output = step(state, program)
        if this_output is not None:
            output.append(str(this_output))

    # print(state.as_str())

    print(",".join(output))

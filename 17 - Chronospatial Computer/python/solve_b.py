from copy import deepcopy
from typing import List

from common import step, read_machine


def valid_substring(output: List[int], program: List[int]):
    if len(output) > len(program):
        return False

    for i in range(0, len(output)):
        if output[i] != program[i]:
            return False

    return True


if __name__ == "__main__":
    initial_state, program = read_machine()

    a = 14827793
    longest = 0
    while True:
        a = a + 8
        state = deepcopy(initial_state)
        state.reg_a = a

        if a % 10000 == 0:
            print(f"reg_a = {state.reg_a}")

        output = []
        seen_states = dict() # Avoid infinite loops
        while state.inst in range(0, len(program)) and valid_substring(output, program):
            # print(state.as_str())

            this_output = step(state, program)
            if this_output is not None:
                output.append(this_output)
                # Changed states, can forget about old ones
                seen_states = dict()

            state_summary = state.as_str() + str(output)
            if state_summary in seen_states:
                break
            seen_states[state_summary] = True

        if len(output) >= longest:
            longest = len(output)
            print(f"a = {a} gives ", output)
            print("    ", state.as_str())
            # exit(0)
        if program == output:
            break

    # print(state.as_str())

    print(a)

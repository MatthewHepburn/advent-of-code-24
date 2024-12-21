from common import step, read_machine

if __name__ == "__main__":
    state, program = read_machine()

    # print(program)

    output = []
    while state.inst in range(0, len(program)):
        # print(state.as_str())

        this_output = step(state, program)
        if this_output is not None:
            output.append(str(this_output))

    # print(state.as_str())

    print(",".join(output))

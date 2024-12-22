import copy

def permutations_with_repetition_fixed_len(values, length: int):
    assert len(values) > 0
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
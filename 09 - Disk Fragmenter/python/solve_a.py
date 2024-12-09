from loader import input_as_string


if __name__ == "__main__":
    input = [int(x) for x in list(input_as_string().strip())]

    disk = []

    next_is_file = True
    next_id = 0
    for x in input:
        next_symbol = next_id if next_is_file else "."
        disk = disk + ([next_symbol] * x)
        if next_is_file:
            next_id = next_id + 1
        next_is_file = not next_is_file

    data_indices = [i for i in range(0, len(disk)) if disk[i] != "."]

    for i in range(0, len(disk)):
        if disk[i] != ".":
            continue

        # Empty space, move our next bit of data here
        old_index = data_indices.pop()
        if old_index <= i:
            break

        # print("Moving from " + str(old_index) + " to " + str(i))
        data = disk[old_index]
        disk[i] = data
        disk[old_index] = "."

        if len(data_indices) == 0:
            break

    # print("".join([str(x) for x in disk]))

    check_sum = sum(disk[i] * i for i in range(0, len(disk)) if disk[i] != '.')
    print(check_sum)
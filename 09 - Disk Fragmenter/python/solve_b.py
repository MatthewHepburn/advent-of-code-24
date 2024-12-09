from re import search
from typing import Union, List

from loader import input_as_string

class Space:
    file_id = None
    def __init__(self, size: int):
        self.size = size

class File:
    def __init__(self, size: int, file_id: int):
        self.size = size
        self.file_id = file_id

if __name__ == "__main__":
    input = [int(x) for x in list(input_as_string().strip())]

    disk: List[Union[File, Space]] = []

    next_is_file = True
    next_id = 0
    for x in input:
        next_data = File(x, next_id) if next_is_file else Space(x)
        disk.append(next_data)
        if next_is_file:
            next_id = next_id + 1
        next_is_file = not next_is_file

    # disk can grow, so we can't do a simple foreach
    search_point = 0
    while search_point < len(disk):
        search_point = search_point + 1
        from_index = len(disk) - search_point
        data = disk[from_index]
        if data.file_id is None:
            continue

        found_dest = False
        to_index = None
        for i in range(0, from_index):
            if disk[i].file_id is None and disk[i].size >= data.size:
                found_dest = True
                to_index = i
                break
        if not found_dest:
            continue

        target_space = disk[to_index]
        leftover_space = Space(target_space.size - data.size) if target_space.size != data.size else None
        disk[from_index] = Space(data.size)
        disk[to_index] = data
        if leftover_space is not None:
            disk.insert(to_index + 1, leftover_space)

    real_disk = []
    for data in disk:
        symbol = data.file_id if data.file_id is not None else "."
        real_disk = real_disk + ([symbol] * data.size)

    # print("".join([str(x) for x in real_disk]))

    check_sum = sum(real_disk[i] * i for i in range(0, len(real_disk)) if real_disk[i] != '.')
    print(check_sum)
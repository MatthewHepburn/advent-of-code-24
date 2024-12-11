from typing import List

from loader import input_as_string

def blink(rock: int) -> List[int]:
    if rock == 0:
        return [1]
    if len(str(rock)) % 2 == 0:
        rock_str = str(rock)
        midpoint = len(rock_str) // 2
        # print("splitting rock:" , rock_str, " at " + str(midpoint))
        part_one = rock_str[:midpoint]
        part_two = rock_str[midpoint:]
        return [int(part_one), int(part_two)]
    return [rock * 2024]

def solve(blinks: int) -> int:
    input = [int(x) for x in input_as_string().split()]
    # print(input)

    rock_counts = dict()
    for rock in input:
        new_count = rock_counts[rock] + 1 if rock in rock_counts else 1
        rock_counts[rock] = new_count
    disk = []

    for i in range(0, blinks):
        new_counts = dict()
        for rock, count in rock_counts.items():
            new_rocks = blink(rock)
            for new_rock in new_rocks:
                new_count = new_counts[new_rock] + count if new_rock in new_counts else count
                new_counts[new_rock] = new_count
        rock_counts = new_counts
        # print(rock_counts)

    sum = 0
    for rock, count in rock_counts.items():
        sum = sum + count

    return sum
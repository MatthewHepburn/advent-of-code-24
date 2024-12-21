import re
from typing import List, Dict

from loader import input_as_strings

def is_possible(towels_by_start: Dict[str, List[str]], target_pattern: str) -> bool:
    frontier = ['']
    while len(frontier) > 0:
        new_frontier = set()
        for pattern in frontier:
            if pattern == target_pattern:
                return True
            if len(pattern) == len(target_pattern):
                continue

            needed_next = target_pattern[len(pattern)]
            options = towels_by_start[needed_next] if needed_next in towels_by_start else []
            for option in options:
                new = pattern + option
                if not target_pattern.startswith(new):
                    continue
                new_frontier.add(new)

        frontier = new_frontier
        # print(frontier)

if __name__ == "__main__":
    input = input_as_strings()

    towels_by_start = dict()

    towels_str = input.pop(0)
    towels = re.findall('[a-z]+', towels_str)
    for towel in towels:
        start = towel[0]
        if not start in towels_by_start:
            towels_by_start[start] = []
        towels_by_start[start].append(towel)

    # print(towels_by_start)
    possible = 0
    for pattern in input:
        pattern = pattern.strip()
        if len(pattern) < 1:
            continue
        if is_possible(towels_by_start, pattern):
            possible = possible + 1
        #     print(f"Pattern '{pattern}' is possible")
        # else:
        #     print(f"Pattern '{pattern}' is NOT possible")

    print(possible)

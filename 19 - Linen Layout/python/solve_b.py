import re
from typing import List, Dict

from loader import input_as_strings

def get_possible_arrangement_count(towels_by_start: Dict[str, List[str]], target_pattern: str) -> int:
    frontier = dict()
    ways = 0
    frontier[''] = 1
    while len(frontier) > 0:
        new_frontier = dict()
        for pattern, count in frontier.items():
            if pattern == target_pattern:
                ways = ways + count
                continue
            if len(pattern) >= len(target_pattern):
                continue

            needed_next = target_pattern[len(pattern)]
            options = towels_by_start[needed_next] if needed_next in towels_by_start else []
            for option in options:
                new = pattern + option
                if not target_pattern.startswith(new):
                    continue
                if not new in new_frontier:
                    new_frontier[new] = 0
                new_frontier[new] = new_frontier[new] + count

        frontier = new_frontier
        # print(frontier)
    return ways

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

        possible = possible + get_possible_arrangement_count(towels_by_start, pattern)
        # print(f"possible = {possible}")
    print(possible)

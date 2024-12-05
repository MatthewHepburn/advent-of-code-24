from typing import List, Dict
from loader import input_as_strings

def is_in_right_order(rules: Dict[int, List[int]], sequence: List[int]) -> bool:
    seen = dict()
    for elem in sequence:
        required_before_list = []
        if elem in rules:
            required_before_list = [before for before in rules[elem] if before in sequence]
        for required_before in required_before_list:
            if not required_before in seen:
                return False
        seen[elem] = True
    return True

def put_in_right_order(rules: Dict[int, List[int]], sequence: List[int]) -> List[int]:
    requirement_dict = dict()
    for elem in sequence:
        required_before_list = []
        if elem in rules:
            required_before_list = [before for before in rules[elem] if before in sequence]
        requirement_dict[elem] = required_before_list

    output = []
    added = dict()
    while len(output) != len(sequence):
        next = None
        for elem, requirements in requirement_dict.items():
            if not [x for x in requirements if x not in added]:
                next = elem
                break
        if next is None:
            raise Exception("Could not order sequence")
        output.append(next)
        added[next] = True
        del requirement_dict[next]

    return output

if __name__ == "__main__":
    input = input_as_strings()

    rules = dict()
    for line in input:
        if not '|' in line:
            continue
        [before_str, after_str] = line.split('|')
        before = int(before_str)
        after = int(after_str)
        if not after in rules:
            rules[after] = []
        rules[after].append(before)


    total = 0
    for line in input:
        if not ',' in line:
            continue
        sequence = [int(x) for x in line.split(',')]
        if not is_in_right_order(rules, sequence):
            ordered = put_in_right_order(rules, sequence)
            total = total + ordered[len(ordered) // 2]

    print(total)


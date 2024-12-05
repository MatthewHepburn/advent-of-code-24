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
                print("Violation! saw " + str(elem) + " without first seeing " + str(required_before))
                return False
        seen[elem] = True
    return True

if __name__ == "__main__":
    input = input_as_strings()

    rules = dict()
    for line in input:
        if not '|' in line:
            continue
        print("Line = '" + line + "'")
        [before_str, after_str] = line.split('|')
        before = int(before_str)
        after = int(after_str)
        if not after in rules:
            rules[after] = []
        rules[after].append(before)


    print(rules)
    total = 0
    for line in input:
        if not ',' in line:
            continue
        sequence = [int(x) for x in line.split(',')]
        if is_in_right_order(rules, sequence):
            print("Right order=", sequence)
            total = total + sequence[len(sequence) // 2]
        else:
            print("Wrong order=", sequence)

    print(total)


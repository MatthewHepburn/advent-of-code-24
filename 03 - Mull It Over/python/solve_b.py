from common import evaluate_mul
from loader import input_as_string
import re

if __name__ == "__main__":
    input = input_as_string()

    matches = re.findall('mul\\([0-9]+,[0-9]+\\)|do\\(\\)|don\'t\\(\\)', input)

    total = 0
    doing = True
    for match in matches:
        if match == 'do()':
            doing = True
            continue
        elif match == 'don\'t()':
            doing = False
            continue

        if doing:
            total += evaluate_mul(match)

    print(total)

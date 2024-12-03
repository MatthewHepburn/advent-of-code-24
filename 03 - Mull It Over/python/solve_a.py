from common import evaluate_mul
from loader import input_as_string
import re

if __name__ == "__main__":
    input = input_as_string()

    matches = re.findall('mul\\([0-9]+,[0-9]+\\)', input)

    total = sum([evaluate_mul(mul) for mul in matches])

    print(total)

from loader import input_as_string
import re

if __name__ == "__main__":
    input = input_as_string(__file__)

    matches = re.findall('mul\\([0-9]+,[0-9]+\\)', input)

    total = 0
    for match in matches:
        factor_strings = re.findall('[0-9]+', match)
        if len(factor_strings) != 2:
            raise Exception("Unexpected length for factor string in " + match)
        total += int(factor_strings[0]) * int(factor_strings[1])

    print(total)

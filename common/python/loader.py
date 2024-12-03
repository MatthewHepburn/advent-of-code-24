import os

from typing import List

def get_file():
    is_example = os.getenv('AOC_EXAMPLE_MODE') == "1"
    if is_example:
        filename = 'exampleInput.txt'
    else:
        filename = 'input.txt'

    input_dir = os.path.dirname(os.getcwd())
    path = os.path.join(input_dir, filename)

    return open(path, "r")

def input_as_strings() -> List[str]:
    f = get_file()
    return f.readlines()

def input_as_string() -> str:
    f = get_file()
    return f.read()

def input_as_ints() -> List[List[int]]:
    strings = input_as_strings()
    output = []
    for string in strings:
        items = [int(x) for x in string.split()]
        output.append(items)
    return output




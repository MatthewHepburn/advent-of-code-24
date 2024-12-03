import os

from typing import List


def get_file(caller_file: str):
    is_example = os.getenv('AOC_EXAMPLE_MODE') == "1"
    if is_example:
        filename = 'exampleInput.txt'
    else:
        filename = 'input.txt'

    caller_dir = os.path.dirname(caller_file)
    input_dir = os.path.dirname(caller_dir)
    path = os.path.join(input_dir, filename)

    return open(path, "r")

def input_as_strings(caller_file: str) -> List[str]:
    f = get_file(caller_file)
    return f.readlines()

def input_as_string(caller_file: str) -> str:
    f = get_file(caller_file)
    return f.read()

def input_as_ints(caller_file: str) -> List[List[int]]:
    strings = input_as_strings(caller_file)
    output = []
    for string in strings:
        items = [int(x) for x in string.split()]
        output.append(items)
    return output




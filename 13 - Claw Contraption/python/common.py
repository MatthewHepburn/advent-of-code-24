import re
from typing import List

from grid import GridVector, GridPoint


class Machine:
    def __init__(self, a_vec: GridVector, b_vec: GridVector, prize: GridPoint):
        self.a_vec = a_vec
        self.b_vec = b_vec
        self.prize = prize

def parse_machines(input: List[str]) -> List[Machine]:
    machines = []

    a_vec = None
    b_vec = None
    for line in input:
        if "Button" in line:
            values = [int(x) for x in re.findall('[0-9]+', line)]
            vec = GridVector(values[0], values[1])
            if "Button A" in line:
                a_vec = vec
            else:
                b_vec = vec
        elif "Prize" in line:
            values = [int(x) for x in re.findall('[0-9]+', line)]
            prize = GridPoint(values[0], values[1])
            if a_vec is None or b_vec is None:
                raise Exception("Parse error! Found Prize without buttons")

            machines.append(Machine(a_vec, b_vec, prize))
            a_vec = None
            b_vec = None

    return machines
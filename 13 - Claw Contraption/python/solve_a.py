import re
from typing import Optional

from grid import GridVector, GridPoint
from loader import input_as_strings

class Machine:
    def __init__(self, a_vec: GridVector, b_vec: GridVector, prize: GridPoint):
        self.a_vec = a_vec
        self.b_vec = b_vec
        self.prize = prize

def get_cheapest_win_from_machine(machine: Machine) -> Optional[int]:
    best = None
    for b in range(0, 100):
        for a in range(0, 100):
            x = a * machine.a_vec.i + b * machine.b_vec.i
            y = a * machine.a_vec.j + b * machine.b_vec.j

            if x == machine.prize.i and y == machine.prize.j:
                cost = b + (3 * a)
                best = cost if best is None or cost < best else best

    return best

if __name__ == "__main__":
    input = [x for x in input_as_strings() if x != ""]

    machines = []

    a_vec = None
    b_vec = None
    prize = None
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

    total = 0
    for machine in machines:
        cost = get_cheapest_win_from_machine(machine)
        if cost is not None:
            # print("Cost = ", cost)
            total = total + cost


    print(total)
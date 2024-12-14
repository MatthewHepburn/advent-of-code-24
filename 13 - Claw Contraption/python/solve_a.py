from typing import Optional

from common import parse_machines, Machine
from loader import input_as_strings


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

    machines = parse_machines(input)

    total = 0
    for machine in machines:
        cost = get_cheapest_win_from_machine(machine)
        if cost is not None:
            # print("Cost = ", cost)
            total = total + cost


    print(total)
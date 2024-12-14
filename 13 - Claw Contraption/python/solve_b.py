from typing import Optional

from common import parse_machines, Machine
from loader import input_as_strings


def get_cheapest_win_from_machine(machine: Machine) -> Optional[int]:
    # Transform notation to match the equation I solved
    a1 = machine.a_vec.i
    a2 = machine.a_vec.j

    b1 = machine.b_vec.i
    b2 = machine.b_vec.j

    d1 = machine.prize.i
    d2 = machine.prize.j

    # First find y
    denominator = b2 * a1 - b1 * a2
    if denominator == 0:
        raise Exception("Cannot divide by zero")
    y = (a1 * d2 - a2 * d1) / denominator

    x = (d1 - y * b1) / a1

    # can only accept integer solutions
    if y != int(y):
        return None

    if x != int(x):
        return None

    return int(y) + (3 * int(x))


if __name__ == "__main__":
    input = [x for x in input_as_strings() if x != ""]

    machines = parse_machines(input)


    total = 0
    for machine in machines:
        # Apply correction factor
        machine.prize.i += 10000000000000
        machine.prize.j += 10000000000000

        cost = get_cheapest_win_from_machine(machine)
        if cost is not None:
            # print("Cost = ", cost)
            total = total + cost


    print(total)
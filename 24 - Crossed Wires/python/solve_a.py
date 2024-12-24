from typing import List, Dict

from loader import input_as_strings


class Connection:
    def __init__(self, input_a : str, input_b: str, output: str, operation: str):
        self.operation = operation
        self.output = output
        self.input_b = input_b
        self.input_a = input_a

    def as_str(self):
        return f"{self.input_a} {self.operation} {self.input_b} -> {self.output}"

    def evaluate(self, a: bool, b: bool) -> bool:
        if self.operation == 'AND':
            return a and b
        if self.operation == 'OR':
            return a or b
        if self.operation == 'XOR':
            return (a or b) and not (a and b)

        raise Exception(f"Unknown operation: {operation}")


if __name__ == "__main__":
    input = input_as_strings()

    wires : Dict[str, bool] = dict()

    connections : List[Connection] = []

    z_wires = set()
    frontier = []
    for line in input:
        if ":" in line:
            wire, value = line.strip().split(': ')
            wires[wire] = value == '1'
            frontier.append(wire)
            if wire.startswith('z'):
                z_wires.add(wire)
        elif "->" in line:
            input_a, operation, input_b, _, output = line.strip().split(' ')
            connections.append(Connection(input_a, input_b, output, operation))
            for wire in [input_a, input_b, output]:
                if wire.startswith('z'):
                    z_wires.add(wire)


    z_wires_left = set()
    for z_wire in z_wires:
        if z_wire not in wires:
            z_wires_left.add(z_wire)

    print(wires)
    for connection in connections:
        print(connection.as_str())

    print(z_wires)
    print(z_wires_left)


    while frontier and z_wires_left:
        new_frontier = []
        for wire in frontier:
            for connection in connections:
                # Do we need a more efficient way of looking up connections by input?
                connection_inputs = [connection.input_a, connection.input_b]
                if not wire in connection_inputs:
                    continue

                if connection.input_a in wires and connection.input_b in wires and connection.output not in wires:
                    input_a_value = wires[connection.input_a]
                    input_b_value = wires[connection.input_b]
                    output_value = connection.evaluate(input_a_value, input_b_value)
                    wires[connection.output] = output_value

                    new_frontier.append(connection.output)
                    if connection.output.startswith('z'):
                        z_wires_left.remove(connection.output)

        frontier = new_frontier


    print(wires)

    z_list = list(z_wires)
    z_list.sort()
    print(z_list)

    z_bin = ''
    for z_wire in z_list:
        z_bin = ('1' if wires[z_wire] else '0') + z_bin

    print(z_bin)

    print(int(z_bin, 2))

    exit(0)

import re
from typing import Dict

from loader import input_as_strings


class Computer:
    neighbours: Dict[str, 'Computer'] = dict()

    def __init__(self, name: str):
        self.name = name
        self.neighbours = dict()

if __name__ == "__main__":
    input = input_as_strings()

    # First build up a dictionary of computes
    computers: Dict[str, Computer] = dict()
    for line in input:
        if not "-" in line:
            continue
        computer_names = re.findall("[a-zA-Z]+", line)
        for computer_name in computer_names:
            if not computer_name in computers:
                computers[computer_name] = Computer(computer_name)

    # Now link them up
    for line in input:
        if not "-" in line:
            continue
        computer_names = re.findall("[a-zA-Z]+", line)
        origin = computers[computer_names[0]]
        dest = computers[computer_names[1]]

        # print(f"Linking {origin.name} <=> {dest.name}")

        origin.neighbours[dest.name] = dest
        dest.neighbours[origin.name] = origin

    # print([name for name in computers.keys()])

    triples = set()
    for name, computer in computers.items():
        for neighbour in computer.neighbours.values():
            neighbours_neighbours = neighbour.neighbours.keys()
            for neighbours_neighbour in neighbours_neighbours:
                if neighbours_neighbour == name:
                    # Ignore neighbours who are us!
                    continue
                # Is this neighbour also our neighbour ?
                if neighbours_neighbour in computer.neighbours:
                    triple = [name, neighbour.name, neighbours_neighbour]
                    triple.sort()
                    triples.add(str(triple))

    historian_triples = set()
    for triple in triples:
        if re.match('.*t[a-zA-Z].*', triple):
            historian_triples.add(triple)

    # trip_list = list(historian_triples)
    # trip_list.sort()
    # print(trip_list)

    print(len(historian_triples))



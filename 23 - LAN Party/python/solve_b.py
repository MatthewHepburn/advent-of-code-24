import re
from typing import Dict

from common import Computer
from loader import input_as_strings


if __name__ == "__main__":
    input = input_as_strings()

    # First build up a dictionary of computers
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

    largest_possible = max([len(c.neighbours) for c in computers.values()])
    print(f"Cannot have more than {largest_possible} computers in the LAN party - based on computer with most connections")


    triples = dict()
    for name, computer in computers.items():
        for neighbour in computer.neighbours.values():
            neighbours_neighbours = neighbour.neighbours.keys()
            for neighbours_neighbour in neighbours_neighbours:
                if neighbours_neighbour == name:
                    # Ignore neighbours who are us!
                    continue
                # Is this neighbour also our neighbour ?
                if neighbours_neighbour in computer.neighbours:
                    triple_key_list = [name, neighbour.name, neighbours_neighbour]
                    triple_key_list.sort()
                    triple_key = str(triple_key_list)
                    if triple_key not in triples:
                        triples[triple_key] = [computer, neighbour, computer.neighbours[neighbours_neighbour]]


    biggest_found = set()
    for computer in computers.values():
        triple_count = 0
        for triple_key in triples.keys():
            if computer.name in triple_key:
                triple_count = triple_count + 1

        # Not necessarily true that our LAN party will be the largest possible set, but assume it is
        if triple_count < largest_possible:
            continue

        this_set = set()
        this_set.add(computer.name)
        possible_sets = dict()
        possible_sets[str([computer.name])] = this_set

        frontier = set()
        frontier.add(computer.name)
        considered = set()
        while len(frontier) > 0:
            print("Considering frontier:", frontier)
            print("Possible sets:", possible_sets)

            new_frontier = set()

            for this_computer_name in frontier:
                this_computer = computers[this_computer_name]
                for neighbour in this_computer.neighbours.values():
                    if neighbour.name in considered:
                        continue
                    considered.add(neighbour.name)
                    new_frontier.add(neighbour.name)

                    has_common_triple = False
                    for triple_key in triples.keys():
                        if this_computer_name in triple_key and neighbour.name in triple_key:
                            has_common_triple = True
                            break

                    if not has_common_triple:
                        continue

                    new_possible_sets = dict()
                    for possible_set_key, possible_set in possible_sets.items():
                        has_connections_to_all = True
                        for candidate in possible_set:
                            if not candidate in neighbour.neighbours:
                                has_connections_to_all = False
                                break

                        # Not adding has to be an option, or we could end up being constrained
                        new_possible_sets[possible_set_key] = possible_set
                        if has_connections_to_all:
                            # can add
                            possible_set.add(neighbour.name)
                            set_key_list = list(possible_set)
                            set_key_list.sort()
                            set_key = str(set_key_list)
                            if set_key not in new_possible_sets:
                                new_possible_sets[set_key] = possible_set

                    possible_sets = new_possible_sets

            frontier = new_frontier

        for possible_set in possible_sets.values():
            if len(possible_set) > len(biggest_found):
                biggest_found = possible_set

        if len(biggest_found) == largest_possible:
            print("Largest possible set found, give up the search!")
            break

    print(biggest_found)
    password_list = list(biggest_found)
    password_list.sort()
    print(",".join(password_list))


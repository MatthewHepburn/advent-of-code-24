from typing import Dict


class Computer:
    neighbours: Dict[str, 'Computer'] = dict()

    def __init__(self, name: str):
        self.name = name
        self.neighbours = dict()
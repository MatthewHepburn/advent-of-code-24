from grid import Direction


def direction_from_symbol(input: str) -> Direction:
    if input == ">":
        return Direction.RIGHT
    if input == "^":
        return Direction.UP
    if input == "<":
        return Direction.LEFT
    if input == "v":
        return Direction.DOWN
    raise Exception("Unknown Direction input: " + input)
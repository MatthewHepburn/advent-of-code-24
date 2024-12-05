import re

def evaluate_mul(mul: str) -> int:
    factor_strings = re.findall('[0-9]+', mul)
    if len(factor_strings) != 2:
        raise Exception("Unexpected length for factor string in " + mul)
    return int(factor_strings[0]) * int(factor_strings[1])
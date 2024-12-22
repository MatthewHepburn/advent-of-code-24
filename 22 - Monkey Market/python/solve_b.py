from typing import List

from combinatorics import permutations_with_repetition_fixed_len
from common import next
from loader import input_as_strings

def get_price(secret: int) -> int:
    return secret % 10


def is_valid_sequence(change_sequence: List[int]):
    possible_prices = list(range(0,9))
    for possible_price in possible_prices:
        price = possible_price
        valid = True
        for change in change_sequence:
            price = price + change
            if not 0 < price <= 9:
                # 0 <= price would be valid, but worthless
                valid = False
                break
        if valid:
            return True

    return False


if __name__ == "__main__":
    input = input_as_strings()
    secrets = [int(x) for x in input if len(input) > 0]

    monkey_price_sequences: List[List[int]] = []
    for secret in secrets:
        price_sequence = [get_price(secret)]
        last_price = price_sequence[0]
        for _ in range(0, 2000):
            secret = next(secret)
            price = get_price(secret)
            price_sequence.append(price)
        monkey_price_sequences.append(price_sequence)

    # print("Computed price sequences")

    change_sequence_values = dict()
    best_bananas = 0
    for price_sequence in monkey_price_sequences:
        last_price = None
        seen = set()
        window = []
        for price in price_sequence:
            if last_price is not None:
                change = price - last_price
                window.append(change)

            if len(window) > 4:
                window.pop(0)

            last_price = price
            if len(window) == 4:
                key = str(window)
                if key not in seen:
                    value = change_sequence_values[key] + price if key in change_sequence_values else price
                    change_sequence_values[key] = value
                    best_bananas = max(best_bananas, value)
                seen.add(key)

    print(best_bananas)



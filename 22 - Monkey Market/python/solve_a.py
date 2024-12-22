from common import next
from loader import input_as_strings


if __name__ == "__main__":
    input = input_as_strings()
    secrets = [int(x) for x in input if len(input) > 0]

    total = 0
    for secret in secrets:
        for _ in range(0, 2000):
            secret = next(secret)
        total = total + secret

    print(total)



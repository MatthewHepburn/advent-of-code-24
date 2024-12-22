def mix(a: int, b: int) -> int:
    return (a | b) & ~(a & b)

def prune(a: int) -> int:
    return a % 16777216

def next(secret: int) -> int:
    a = secret * 64
    secret = mix(secret, a)
    secret = prune(secret)

    b = secret // 32
    secret = mix(secret, b)
    secret = prune(secret)

    c = secret * 2048
    secret = mix(secret, c)
    secret = prune(secret)

    return secret
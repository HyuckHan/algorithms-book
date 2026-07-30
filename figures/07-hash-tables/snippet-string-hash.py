def ascii_sum(s):
    return sum(ord(c) for c in s)


def string_hash(s, base=131):
    h = 0
    for c in s:
        h = h * base + ord(c)
    return h

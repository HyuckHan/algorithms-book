def build_horspool_shift(pattern):
    m = len(pattern)
    shift = {}
    fallback = m if m else 1
    for j in range(m - 1):
        shift[pattern[j]] = m - 1 - j
    return shift, fallback


def horspool_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return [0]
    if m > n:
        return []
    shift, fallback = build_horspool_shift(pattern)
    result = []
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            result.append(s)
        s += shift.get(text[s + m - 1], fallback)
    return result

def naive_match(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return [0]
    result = []
    for s in range(n - m + 1):
        j = 0
        while j < m and text[s + j] == pattern[j]:
            j += 1
        if j == m:
            result.append(s)
    return result

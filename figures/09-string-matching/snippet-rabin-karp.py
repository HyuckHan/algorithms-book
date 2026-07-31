def rabin_karp(text, pattern, base, modulus):
    n, m = len(text), len(pattern)
    if m == 0:
        return [0]
    if m > n:
        return []
    h = 1
    for _ in range(1, m):
        h = _mul_mod(h, base, modulus)
    p_hash = t_hash = 0
    for j in range(m):
        p_hash = _add_mod(_mul_mod(p_hash, base, modulus), _code(pattern[j]), modulus)
        t_hash = _add_mod(_mul_mod(t_hash, base, modulus), _code(text[j]), modulus)
    result = []
    for s in range(n - m + 1):
        if p_hash == t_hash and text[s:s + m] == pattern:
            result.append(s)
        if s < n - m:
            leading = _mul_mod(_code(text[s]), h, modulus)
            t_hash = _add_mod(_mul_mod(base, _sub_mod(t_hash, leading, modulus), modulus),
                               _code(text[s + m]), modulus)
    return result

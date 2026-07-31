"""String matching library: Naive, Rabin-Karp, KMP (BuildLPS+search), Horspool
(BuildShiftTable+search). Policy: 0-based indexing, empty pattern all-match is
[0], m>n is no match. Matches lecture-notes/code/lecture09's
StringMatchers.java/string_matching.c same policy and example inputs."""


# snippet:naive-match:start
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
# snippet:naive-match:end


def _add_mod(a, b, q):
    a %= q
    b %= q
    return a - (q - b) if a >= q - b else a + b


def _sub_mod(a, b, q):
    a %= q
    b %= q
    return a - b if a >= b else q - (b - a)


def _mul_mod(a, b, q):
    a %= q
    b %= q
    result = 0
    while b:
        if b & 1:
            result = _add_mod(result, a, q)
        a = _add_mod(a, a, q)
        b >>= 1
    return result


def _code(c):
    return ord(c) + 1


# snippet:rabin-karp:start
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
# snippet:rabin-karp:end


# snippet:kmp:start
def build_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return [0]
    lps = build_lps(pattern)
    result = []
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                result.append(i - m)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return result
# snippet:kmp:end


# snippet:horspool:start
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
# snippet:horspool:end

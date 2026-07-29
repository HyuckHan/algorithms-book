def counting_sort_by_digit(A, exp):
    n = len(A)
    out = [0] * n
    count = [0] * 10
    for x in A:
        count[(x // exp) % 10] += 1
    for d in range(1, 10):
        count[d] += count[d - 1]
    for i in range(n - 1, -1, -1):
        digit = (A[i] // exp) % 10
        count[digit] -= 1
        out[count[digit]] = A[i]
    return out

def radix_sort(A):
    A = A[:]
    max_val = max(A)
    exp = 1
    while max_val // exp > 0:
        A = counting_sort_by_digit(A, exp)
        exp *= 10
    return A

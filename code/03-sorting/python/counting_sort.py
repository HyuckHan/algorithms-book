"""Counting Sort (1.6.1)."""

# snippet:counting-sort:start
def counting_sort(A, k):
    # A is 0-based; internally builds 1-based working arrays (index 0
    # unused, matching the pseudocode's A[1..n]) so the prefix-sum C array
    # and the place-then-decrement order carry over unchanged.
    n = len(A)
    Ain = [0] + A[:]
    C = [0] * (k + 1)
    for j in range(1, n + 1):
        C[Ain[j]] += 1
    for i in range(1, k + 1):
        C[i] += C[i - 1]
    B = [0] * (n + 1)
    for j in range(n, 0, -1):
        B[C[Ain[j]]] = Ain[j]
        C[Ain[j]] -= 1
    return B[1:]
# snippet:counting-sort:end

if __name__ == "__main__":
    data = [4, 1, 3, 4, 3]
    k = 4
    print("input:", ",".join(str(x) for x in data))
    print("counting:", ",".join(str(x) for x in counting_sort(data, k)))

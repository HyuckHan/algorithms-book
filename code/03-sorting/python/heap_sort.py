"""MAX-HEAPIFY / BUILD-MAX-HEAP / Heapsort (1.5.3)."""

# snippet:heap-sort:start
def max_heapify(A, i, heap_size):
    # A is 1-based (index 0 unused) to match this section's Index
    # convention (parent(i)=i/2, left(i)=2i, right(i)=2i+1) exactly.
    l, r, largest = 2 * i, 2 * i + 1, i
    if l <= heap_size and A[l] > A[largest]:
        largest = l
    if r <= heap_size and A[r] > A[largest]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest, heap_size)

def build_max_heap(A, n):
    for i in range(n // 2, 0, -1):
        max_heapify(A, i, n)

def heap_sort(A):
    # A is an ordinary 0-based list; internally this builds a 1-based
    # working copy (index 0 unused) so the pseudocode's index arithmetic
    # carries over unchanged, then strips the sentinel before returning.
    n = len(A)
    H = [0] + A[:]
    build_max_heap(H, n)
    for last in range(n, 1, -1):
        H[1], H[last] = H[last], H[1]
        max_heapify(H, 1, last - 1)
    return H[1:]
# snippet:heap-sort:end

if __name__ == "__main__":
    data = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
    print("input:", ",".join(str(x) for x in data))
    print("heapsort:", ",".join(str(x) for x in heap_sort(data)))

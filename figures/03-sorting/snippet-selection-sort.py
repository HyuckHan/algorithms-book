def selection_sort(A):
    A = A[:]; n = len(A); comps = 0
    for last in range(n - 1, 0, -1):
        m = 0
        for i in range(1, last + 1):
            comps += 1
            if A[i] > A[m]:
                m = i
        A[m], A[last] = A[last], A[m]
    return A, comps

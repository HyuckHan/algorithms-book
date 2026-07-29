def bubble_sort(A):
    A = A[:]; n = len(A); swaps = 0
    for last in range(n - 1, 0, -1):
        swapped = False
        for i in range(last):
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i]
                swapped = True; swaps += 1
        if not swapped:
            break
    return A, swaps

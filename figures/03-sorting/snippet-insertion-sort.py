def insertion_sort(A):
    A = A[:]; shifts = 0
    for i in range(1, len(A)):
        key = A[i]; j = i - 1
        while j >= 0 and A[j] > key:      # shift 횟수 == inversion 수
            A[j + 1] = A[j]; j -= 1; shifts += 1
        A[j + 1] = key
    return A, shifts

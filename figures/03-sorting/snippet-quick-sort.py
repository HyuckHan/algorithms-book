def partition(A, low, high):
    pivot = A[high]; i = low - 1
    for j in range(low, high):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[high] = A[high], A[i + 1]
    return i + 1

def quick_sort(A, low=0, high=None):
    if high is None:
        A = A[:]; high = len(A) - 1
    if low < high:
        p = partition(A, low, high)
        quick_sort(A, low, p - 1)
        quick_sort(A, p + 1, high)
    return A

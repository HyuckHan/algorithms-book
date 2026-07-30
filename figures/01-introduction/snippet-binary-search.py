def binary_search(A, x):
    low, high = 0, len(A) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if A[mid] == x:
            return mid
        elif A[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1  # NOT_FOUND

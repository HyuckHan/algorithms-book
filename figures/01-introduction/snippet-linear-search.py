def linear_search(A, x):
    for i in range(len(A)):
        if A[i] == x:
            return i
    return -1  # NOT_FOUND

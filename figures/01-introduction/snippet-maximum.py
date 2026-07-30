def maximum(A):
    v = A[0]
    for i in range(1, len(A)):
        if A[i] > v:
            v = A[i]
    return v

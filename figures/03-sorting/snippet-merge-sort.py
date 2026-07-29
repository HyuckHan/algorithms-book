def merge(L, R):
    out = []; i = j = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: out.append(L[i]); i += 1   # <= 라서 stable
        else:            out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:]); return out

def merge_sort(A):
    if len(A) <= 1: return A
    mid = len(A) // 2
    return merge(merge_sort(A[:mid]), merge_sort(A[mid:]))

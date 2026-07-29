"""Selection/Bubble/Insertion/Merge/Quick Sort. Java/C 참조 구현과 동일한 예제 입력을 쓴다."""

# snippet:selection-sort:start
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
# snippet:selection-sort:end

# snippet:bubble-sort:start
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
# snippet:bubble-sort:end

# snippet:insertion-sort:start
def insertion_sort(A):
    A = A[:]; shifts = 0
    for i in range(1, len(A)):
        key = A[i]; j = i - 1
        while j >= 0 and A[j] > key:      # shift 횟수 == inversion 수
            A[j + 1] = A[j]; j -= 1; shifts += 1
        A[j + 1] = key
    return A, shifts
# snippet:insertion-sort:end

# snippet:merge-sort:start
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
# snippet:merge-sort:end

# snippet:quick-sort:start
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
# snippet:quick-sort:end

if __name__ == "__main__":
    data = [29, 10, 14, 37, 13, 5, 21, 8]
    print("input   :", data)
    print("selection:", selection_sort(data)[0])
    print("bubble   :", bubble_sort(data)[0])
    print("insertion:", insertion_sort(data)[0])
    print("merge    :", merge_sort(data))
    print("quick    :", quick_sort(data))

"""Recursive Binary Search."""

# snippet:recursive-binary-search:start
def bsearch(A, x, begin, end):
    # Base case: begin > end (empty interval, -1, no further call).
    # Recursive case: narrow to one inclusive half [begin,mid-1] or
    # [mid+1,end], progress measure end-begin strictly decreasing. Max
    # call-stack depth is Theta(log n). mid uses the overflow-safe
    # `begin + (end-begin)//2` form (not needed for Python's arbitrary-size
    # ints, but kept for parity with the C/Java versions).
    if begin > end:
        return -1
    mid = begin + (end - begin) // 2
    if A[mid] == x:
        return mid
    if x < A[mid]:
        return bsearch(A, x, begin, mid - 1)
    return bsearch(A, x, mid + 1, end)
# snippet:recursive-binary-search:end

if __name__ == "__main__":
    data = [2, 5, 8, 12, 16, 23, 38]
    x = 16
    print("input:", ",".join(str(v) for v in data))
    print("x:", x)
    print("bsearch:", bsearch(data, x, 0, len(data) - 1))

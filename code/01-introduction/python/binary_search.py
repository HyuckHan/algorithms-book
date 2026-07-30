"""Binary Search."""

# snippet:binary-search:start
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
# snippet:binary-search:end

if __name__ == "__main__":
    data = [3, 6, 9, 12, 15, 18, 21, 24]
    x = 18
    print("input:", ",".join(str(v) for v in data))
    print("x:", x)
    print("binary:", binary_search(data, x))

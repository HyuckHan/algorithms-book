"""Linear Search."""

# snippet:linear-search:start
def linear_search(A, x):
    for i in range(len(A)):
        if A[i] == x:
            return i
    return -1  # NOT_FOUND
# snippet:linear-search:end

if __name__ == "__main__":
    data = [3, 6, 9, 12, 15, 18, 21, 24]
    x = 12
    print("input:", ",".join(str(v) for v in data))
    print("x:", x)
    print("linear:", linear_search(data, x))

"""Maximum."""

# snippet:maximum:start
def maximum(A):
    v = A[0]
    for i in range(1, len(A)):
        if A[i] > v:
            v = A[i]
    return v
# snippet:maximum:end

if __name__ == "__main__":
    data = [7, 12, 3, 15, 8]
    print("input:", ",".join(str(v) for v in data))
    print("maximum:", maximum(data))

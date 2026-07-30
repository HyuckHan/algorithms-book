"""sum(n) = 1 + 2 + ... + n."""

# snippet:sum:start
def sum_(n):
    # Base case: n == 0 (returns 0, no further call). Recursive case:
    # n + sum(n-1), progress measure n -> n-1. Max call-stack depth is n+1
    # (sum(n), sum(n-1), ..., sum(0)), matching the push trace in this
    # section for sum(4).
    if n == 0:
        return 0
    return n + sum_(n - 1)
# snippet:sum:end

if __name__ == "__main__":
    n = 4
    print("input: n=%d" % n)
    print("sum:", sum_(n))

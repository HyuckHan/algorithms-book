"""F(0)=0, F(1)=1. Same recurrence and evaluation order as FibMemo/FibBottomUp
in the lecture notes (see lecture-notes/code/lecture05/c/fibonacci.c and
java/FibonacciDP.java) -- newly written in Python, no canonical source exists."""


# snippet:fib-memo:start
def fib_memo(n, memo=None):
    if memo is None:
        memo = {0: 0, 1: 1}
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
# snippet:fib-memo:end


# snippet:fib-bottom-up:start
def fib_bottom_up(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        current = prev2 + prev1
        prev2, prev1 = prev1, current
    return prev1
# snippet:fib-bottom-up:end


if __name__ == "__main__":
    n = 6
    print("n:", n)
    print("memo:", fib_memo(n))
    print("bottom_up:", fib_bottom_up(n))

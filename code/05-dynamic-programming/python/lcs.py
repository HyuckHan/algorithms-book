"""Same recurrence and tie-break (up preferred on tie) as the "LCS Bottom-Up"
pseudocode, and the C/Java demos in this chapter -- newly written in Python,
no canonical source exists."""


# snippet:lcs-bottom-up:start
def lcs_bottom_up(x, y):
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            result.append(x[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(result))
# snippet:lcs-bottom-up:end


if __name__ == "__main__":
    x, y = "ABCBDAB", "BDCABA"
    s = lcs_bottom_up(x, y)
    print("X:", x)
    print("Y:", y)
    print("lcs:", s)
    print("length:", len(s))

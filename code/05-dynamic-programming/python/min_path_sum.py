"""Same recurrence and tie-break (up preferred on tie) as MinPathMemo/the
Bottom-Up Evaluation Order pseudocode, and the C/Java demos in this chapter
-- newly written in Python, no canonical source exists."""


# snippet:min-path-memo:start
def min_path_memo(a, memo=None, seen=None, i=None, j=None):
    rows, cols = len(a), len(a[0])
    if memo is None:
        memo = [[0] * cols for _ in range(rows)]
        seen = [[False] * cols for _ in range(rows)]
        i, j = rows - 1, cols - 1
    if seen[i][j]:
        return memo[i][j]
    if i == 0 and j == 0:
        result = a[0][0]
    elif i == 0:
        result = min_path_memo(a, memo, seen, i, j - 1) + a[i][j]
    elif j == 0:
        result = min_path_memo(a, memo, seen, i - 1, j) + a[i][j]
    else:
        up = min_path_memo(a, memo, seen, i - 1, j)
        left = min_path_memo(a, memo, seen, i, j - 1)
        result = (up if up <= left else left) + a[i][j]
    seen[i][j] = True
    memo[i][j] = result
    return result
# snippet:min-path-memo:end


# snippet:matrix-bottom-up:start
def min_path_bottom_up(a):
    rows, cols = len(a), len(a[0])
    dp = [[0] * cols for _ in range(rows)]
    parent = [[0] * cols for _ in range(rows)]  # 1=up, 2=left
    dp[0][0] = a[0][0]
    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + a[0][j]
        parent[0][j] = 2
    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + a[i][0]
        parent[i][0] = 1
    for i in range(1, rows):
        for j in range(1, cols):
            up, left = dp[i - 1][j], dp[i][j - 1]
            if up <= left:
                dp[i][j], parent[i][j] = up + a[i][j], 1
            else:
                dp[i][j], parent[i][j] = left + a[i][j], 2
    path = []
    i, j = rows - 1, cols - 1
    while True:
        path.append((i, j))
        if i == 0 and j == 0:
            break
        if parent[i][j] == 1:
            i -= 1
        else:
            j -= 1
    path.reverse()
    return dp[rows - 1][cols - 1], path
# snippet:matrix-bottom-up:end


if __name__ == "__main__":
    m = [[6, 7, 12, 5], [5, 3, 11, 18], [7, 17, 3, 3], [8, 10, 14, 9]]
    print("memo sum:", min_path_memo(m))
    total, path = min_path_bottom_up(m)
    print("bottom_up sum:", total)
    print("path:", " ".join("(%d,%d)" % (r + 1, c + 1) for r, c in path))

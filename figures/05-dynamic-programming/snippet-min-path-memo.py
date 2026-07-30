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

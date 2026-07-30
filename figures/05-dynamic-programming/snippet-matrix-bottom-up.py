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

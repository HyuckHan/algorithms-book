def solve_n_queens(n):
    solutions = []
    position = [0] * n
    used_col = [False] * n
    diag1 = [False] * (2 * n - 1) if n > 0 else []
    diag2 = [False] * (2 * n - 1) if n > 0 else []

    def place(row):
        if row == n:
            solutions.append(tuple(position))
            return
        for col in range(n):
            a = row - col + n - 1
            b = row + col
            if used_col[col] or diag1[a] or diag2[b]:
                continue
            used_col[col] = diag1[a] = diag2[b] = True
            position[row] = col
            place(row + 1)
            used_col[col] = diag1[a] = diag2[b] = False

    if n == 0:
        return [()]
    place(0)
    return solutions

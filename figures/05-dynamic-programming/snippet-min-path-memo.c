static long long min_path_memo_rec(const long long *a, size_t cols, int i, int j, long long *memo, bool *seen) {
    size_t k = (size_t)i * cols + (size_t)j;
    if (seen[k]) return memo[k];
    long long result;
    if (i == 0 && j == 0) {
        result = a[k];
    } else if (i == 0) {
        result = min_path_memo_rec(a, cols, i, j - 1, memo, seen) + a[k];
    } else if (j == 0) {
        result = min_path_memo_rec(a, cols, i - 1, j, memo, seen) + a[k];
    } else {
        long long up = min_path_memo_rec(a, cols, i - 1, j, memo, seen);
        long long left = min_path_memo_rec(a, cols, i, j - 1, memo, seen);
        result = (up <= left ? up : left) + a[k];
    }
    seen[k] = true;
    memo[k] = result;
    return result;
}

static bool min_path_memo(const long long *a, size_t rows, size_t cols, long long *out) {
    if (!a || !out || rows == 0 || cols == 0) return false;
    size_t n = rows * cols;
    long long *memo = malloc(n * sizeof(*memo));
    bool *seen = calloc(n, sizeof(*seen));
    if (!memo || !seen) { free(memo); free(seen); return false; }
    *out = min_path_memo_rec(a, cols, (int)rows - 1, (int)cols - 1, memo, seen);
    free(memo); free(seen);
    return true;
}

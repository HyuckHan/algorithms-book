static long long memo_rec(int n, long long *memo) {
    if (memo[n] != LLONG_MIN) return memo[n];
    memo[n] = memo_rec(n - 1, memo) + memo_rec(n - 2, memo);
    return memo[n];
}

static bool fib_memo(int n, long long *out) {
    if (!out || n < 0 || n > 92) return false;
    long long *memo = calloc((size_t)n + 1, sizeof(*memo));
    if (!memo) return false;
    for (int i = 0; i <= n; ++i) memo[i] = LLONG_MIN;
    memo[0] = 0;
    if (n >= 1) memo[1] = 1;
    *out = memo_rec(n, memo);
    free(memo); return true;
}

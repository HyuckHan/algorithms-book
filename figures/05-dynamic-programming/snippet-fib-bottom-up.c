static bool fib_bottom_up(int n, long long *out) {
    if (!out || n < 0 || n > 92) return false;
    if (n <= 1) { *out = n; return true; }
    long long prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; ++i) {
        long long current = prev2 + prev1;
        prev2 = prev1; prev1 = current;
    }
    *out = prev1; return true;
}

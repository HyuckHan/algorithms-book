    public static long fibBottomUp(int n) {
        if (n < 0 || n > 92) throw new IllegalArgumentException("n must be 0..92");
        if (n <= 1) return n;
        long prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++) { long cur = Math.addExact(prev2, prev1); prev2 = prev1; prev1 = cur; }
        return prev1;
    }

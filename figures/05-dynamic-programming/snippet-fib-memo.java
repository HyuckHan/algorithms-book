    private static long memoRec(int n, long[] memo) {
        if (memo[n] != Long.MIN_VALUE) return memo[n];
        memo[n] = Math.addExact(memoRec(n - 1, memo), memoRec(n - 2, memo));
        return memo[n];
    }

    public static long fibMemo(int n) {
        if (n < 0 || n > 92) throw new IllegalArgumentException("n must be 0..92");
        long[] memo = new long[n + 1];
        Arrays.fill(memo, Long.MIN_VALUE);
        memo[0] = 0;
        if (n >= 1) memo[1] = 1;
        return memoRec(n, memo);
    }

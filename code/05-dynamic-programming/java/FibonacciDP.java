import java.util.Arrays;

public final class FibonacciDP {
    private FibonacciDP() {}

    // Reused verbatim from lecture-notes/code/lecture05/java/FibonacciDP.java
    // (fibMemo/memoRec), renamed only to match this chapter's pseudocode
    // block names.
    // snippet:fib-memo:start
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
    // snippet:fib-memo:end

    // snippet:fib-bottom-up:start
    public static long fibBottomUp(int n) {
        if (n < 0 || n > 92) throw new IllegalArgumentException("n must be 0..92");
        if (n <= 1) return n;
        long prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++) { long cur = Math.addExact(prev2, prev1); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
    // snippet:fib-bottom-up:end

    public static void main(String[] args) {
        int n = 6;
        System.out.println("n: " + n);
        System.out.println("memo: " + fibMemo(n));
        System.out.println("bottom_up: " + fibBottomUp(n));
    }
}

#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

/* F(0)=0, F(1)=1. Valid through n=92 for signed long long.
 * Reused verbatim from lecture-notes/code/lecture05/c/fibonacci.c
 * (fib_memo/memo_rec), renamed only to match this chapter's pseudocode
 * block names (FibMemo, FibBottomUp). */

// snippet:fib-memo:start
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
// snippet:fib-memo:end

// snippet:fib-bottom-up:start
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
// snippet:fib-bottom-up:end

int main(void) {
    int n = 6;
    long long memo_result = -1, bottom_up_result = -1;
    fib_memo(n, &memo_result);
    fib_bottom_up(n, &bottom_up_result);
    printf("n: %d\n", n);
    printf("memo: %lld\n", memo_result);
    printf("bottom_up: %lld\n", bottom_up_result);
    return 0;
}

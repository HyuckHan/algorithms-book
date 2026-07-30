/* sum(n) = 1 + 2 + ... + n. Base case: n == 0 (returns 0, no further call).
 * Recursive case: n + sum(n-1), progress measure n -> n-1. Max call-stack
 * depth is n+1 (sum(n), sum(n-1), ..., sum(0)), matching the push trace in
 * this section for sum(4). */
static int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}

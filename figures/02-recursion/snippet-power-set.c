/* Power Set. Base case: k == n (all n elements decided; prints the
 * current selection, including the empty set). Recursive case: exclude
 * data[k] first, then include it -- this exclude-before-include order at
 * every level makes the printed order match the state-space tree's
 * left-to-right leaf order exactly (see 13-power-set-tree). Progress
 * measure: k -> k+1. Max call-stack depth is n. `include` is a
 * caller-owned array (no global state), threaded through by pointer. */
static void power_set(int k, int n, bool *include) {
    if (k == n) {
        print_selected(include);
        return;
    }
    include[k] = false;
    power_set(k + 1, n, include);
    include[k] = true;
    power_set(k + 1, n, include);
}

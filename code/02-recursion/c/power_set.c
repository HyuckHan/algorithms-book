#include <stdio.h>
#include <stdbool.h>

#define N 3
static const char DATA[N] = {'a', 'b', 'c'};

static void print_selected(const bool *include) {
    printf("{");
    bool first = true;
    for (int i = 0; i < N; i++) {
        if (include[i]) {
            if (!first) printf(",");
            printf("%c", DATA[i]);
            first = false;
        }
    }
    printf("}\n");
}

// snippet:power-set:start
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
// snippet:power-set:end

int main(void) {
    bool include[N] = {false, false, false};
    printf("input: {a,b,c}\n");
    power_set(0, N, include);
    return 0;
}

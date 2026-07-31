#include "state_space_search.h"
#include <stdio.h>

int main(void) {
    const int64_t weights[] = {3, 4, 5, 6};
    uint64_t masks[16];
    size_t count;
    ss_metrics m;
    if (ss_subset_sum_masks(weights, 4, 9, masks, 16, &count, true, &m) != SS_OK) return 1;
    printf("solutions: %zu\n", count);
    return 0;
}

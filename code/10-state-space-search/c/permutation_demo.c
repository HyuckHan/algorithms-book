#include "state_space_search.h"
#include <stdio.h>

int main(void) {
    uint64_t perms, combos;
    ss_metrics m;
    if (ss_permutation_count(5, 4, &perms, &m) != SS_OK) return 1;
    if (ss_combination_count(5, 4, &combos, &m) != SS_OK) return 1;
    printf("P(5,4): %llu\n", (unsigned long long)perms);
    printf("C(5,4): %llu\n", (unsigned long long)combos);
    return 0;
}

#include "state_space_search.h"
#include <stdio.h>

int main(void) {
    uint64_t n4, n8;
    ss_metrics m;
    if (ss_n_queens_count(4, &n4, &m) != SS_OK) return 1;
    if (ss_n_queens_count(8, &n8, &m) != SS_OK) return 1;
    printf("N(4): %llu\n", (unsigned long long)n4);
    printf("N(8): %llu\n", (unsigned long long)n8);
    return 0;
}

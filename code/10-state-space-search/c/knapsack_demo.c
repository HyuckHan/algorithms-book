#include "state_space_search.h"
#include <stdio.h>

int main(void) {
    const ss_item items[] = {{2,40}, {5,30}, {10,50}, {5,10}};
    ss_knapsack_result result;
    if (ss_knapsack_bnb(items, 4, 16, &result) != SS_OK) return 1;
    printf("profit: %lld\n", (long long)result.profit);
    printf("weight: %lld\n", (long long)result.weight);
    return 0;
}

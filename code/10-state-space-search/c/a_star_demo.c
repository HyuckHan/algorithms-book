#include "state_space_search.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    /* 5x7 grid, obstacles, S at (0,0), G at (4,6) -- the lecture's own example. */
    const size_t rows = 5, cols = 7;
    unsigned char blocked[35];
    memset(blocked, 0, sizeof blocked);
    size_t obstacle_r[] = {0,1,2,2,2,3};
    size_t obstacle_c[] = {3,3,1,2,3,5};
    for (size_t i = 0; i < 6; i++) blocked[obstacle_r[i]*cols + obstacle_c[i]] = 1;

    int64_t cost, dijkstra_cost;
    ss_metrics m;
    if (ss_astar_grid(blocked, rows, cols, 0, 4*cols+6, false, &cost, &m) != SS_OK) return 1;
    printf("cost: %lld\n", (long long)cost);
    if (ss_astar_grid(blocked, rows, cols, 0, 4*cols+6, true, &dijkstra_cost, &m) != SS_OK) return 1;
    printf("dijkstra_cost: %lld\n", (long long)dijkstra_cost);
    return 0;
}

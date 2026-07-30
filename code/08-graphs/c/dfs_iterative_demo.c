#include "graph.h"
#include <stdio.h>

int main(void) {
    Graph *g = graph_create(8, false);
    size_t edges[][2] = {{0,1},{0,2},{0,3},{1,4},{2,4},{2,5},{3,6},{4,7},{6,7}};
    for (size_t i = 0; i < 9; i++) graph_add_edge(g, edges[i][0], edges[i][1], 1);

    size_t order[8];
    graph_dfs_iterative(g, 0, order);
    printf("iterative dfs visit order:");
    for (size_t i = 0; i < 8; i++) printf(" %zu", order[i]);
    printf("\n");

    graph_destroy(g);
    return 0;
}

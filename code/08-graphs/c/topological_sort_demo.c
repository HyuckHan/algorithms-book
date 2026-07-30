#include "graph.h"
#include <stdio.h>

int main(void) {
    Graph *dag = graph_create(6, true);
    size_t edges[][2] = {{0,1},{0,3},{1,2},{1,4},{2,5},{3,5},{4,5}};
    for (size_t i = 0; i < 7; i++) graph_add_edge(dag, edges[i][0], edges[i][1], 1);

    size_t kahn_order[6];
    graph_topological_kahn(dag, kahn_order);
    printf("kahn order:");
    for (size_t i = 0; i < 6; i++) printf(" %zu", kahn_order[i]);
    printf("\n");

    size_t dfs_order[6];
    graph_topological_dfs(dag, dfs_order);
    printf("dfs-topo order:");
    for (size_t i = 0; i < 6; i++) printf(" %zu", dfs_order[i]);
    printf("\n");
    graph_destroy(dag);

    Graph *cycle = graph_create(3, true);
    graph_add_edge(cycle, 0, 1, 1); graph_add_edge(cycle, 1, 2, 1); graph_add_edge(cycle, 2, 0, 1);
    size_t out[3];
    printf("cycle graph kahn detects cycle: %s\n", graph_topological_kahn(cycle, out) ? "false" : "true");
    printf("cycle graph dfs-topo detects cycle: %s\n", graph_topological_dfs(cycle, out) ? "false" : "true");
    graph_destroy(cycle);
    return 0;
}

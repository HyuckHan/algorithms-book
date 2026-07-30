#include "graph.h"
#include <stdio.h>

int main(void) {
    const char *name = "sabc";
    Graph *g = graph_create(4, true);
    long long e[][3] = {{0,1,3},{0,2,2},{1,3,-4},{2,3,1}};
    for (size_t i = 0; i < 4; i++) graph_add_edge(g, (size_t)e[i][0], (size_t)e[i][1], e[i][2]);

    int64_t dist[4]; ptrdiff_t parent[4];
    graph_dag_shortest_paths(g, 0, dist, parent);
    printf("dist:");
    for (size_t i = 0; i < 4; i++) printf(" %lld", (long long)dist[i]);
    printf("\n");

    size_t path[4], len = 0;
    graph_reconstruct_path(4, 0, 3, parent, path, &len);
    printf("path to c:");
    for (size_t i = 0; i < len; i++) printf("%s%c", i ? " -> " : " ", name[path[i]]);
    printf("\n");

    graph_destroy(g);
    return 0;
}

#include "graph.h"
#include <stdio.h>

int main(void) {
    const char *sname = "SABCDE";
    Graph *g = graph_create(6, true);
    long long e[][3] = {{0,1,4},{0,2,2},{2,1,1},{1,3,5},{2,3,8},
        {2,4,10},{3,4,2},{3,5,6},{4,5,3}};
    for (size_t i = 0; i < 9; i++) graph_add_edge(g, (size_t)e[i][0], (size_t)e[i][1], e[i][2]);

    int64_t dist[6]; ptrdiff_t parent[6];
    graph_dijkstra(g, 0, dist, parent);
    printf("dijkstra dist:");
    for (size_t i = 0; i < 6; i++) printf(" %lld", (long long)dist[i]);
    printf("\n");
    size_t path[6], len = 0;
    graph_reconstruct_path(6, 0, 5, parent, path, &len);
    printf("dijkstra path to E:");
    for (size_t i = 0; i < len; i++) printf("%s%c", i ? " -> " : " ", sname[path[i]]);
    printf("\n");
    graph_destroy(g);

    const char *bfname = "sabcd";
    Graph *bf = graph_create(5, true);
    long long be[][3] = {{3,4,2},{1,3,-2},{2,3,3},{0,1,4},{0,2,5},{2,4,6}};
    for (size_t i = 0; i < 6; i++) graph_add_edge(bf, (size_t)be[i][0], (size_t)be[i][1], be[i][2]);
    int64_t bdist[5]; ptrdiff_t bparent[5]; bool neg = false;
    graph_bellman_ford(bf, 0, bdist, bparent, &neg);
    printf("bellman-ford dist:");
    for (size_t i = 0; i < 5; i++) printf(" %lld", (long long)bdist[i]);
    printf("\n");
    size_t bpath[5], blen = 0;
    graph_reconstruct_path(5, 0, 4, bparent, bpath, &blen);
    printf("bellman-ford path to d:");
    for (size_t i = 0; i < blen; i++) printf("%s%c", i ? " -> " : " ", bfname[bpath[i]]);
    printf("\n");
    graph_destroy(bf);

    Graph *neggraph = graph_create(3, true);
    graph_add_edge(neggraph, 0, 1, 1); graph_add_edge(neggraph, 1, 2, -2); graph_add_edge(neggraph, 2, 1, -2);
    int64_t nd[3]; ptrdiff_t np[3]; bool ncyc = false;
    graph_bellman_ford(neggraph, 0, nd, np, &ncyc);
    printf("reachable negative cycle detected: %s\n", ncyc ? "true" : "false");
    graph_destroy(neggraph);
    return 0;
}

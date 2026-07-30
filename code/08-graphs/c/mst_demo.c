#include "graph.h"
#include <stdio.h>

static void print_edges(const char *label, const MstResult *r) {
    const char *name = "ABCDEFG";
    printf("%s:", label);
    for (size_t i = 0; i < r->count; i++)
        printf(" %c%c%lld", name[r->edges[i].u], name[r->edges[i].v], (long long)r->edges[i].weight);
    printf("\n");
}

int main(void) {
    Graph *g = graph_create(7, false);
    long long e[][3] = {{0,1,8},{0,2,9},{0,3,11},{1,4,10},{2,3,13},
        {2,4,5},{2,5,12},{3,5,8},{3,6,8},{5,6,7}};
    for (size_t i = 0; i < 10; i++) graph_add_edge(g, (size_t)e[i][0], (size_t)e[i][1], e[i][2]);

    MstResult p = {0}, k = {0};
    graph_prim(g, 0, &p);
    print_edges("prim edges", &p);
    printf("prim weight: %lld\n", (long long)p.weight);

    graph_kruskal(g, &k);
    print_edges("kruskal edges", &k);
    printf("kruskal weight: %lld\n", (long long)k.weight);

    mst_result_destroy(&p); mst_result_destroy(&k);
    graph_destroy(g);
    return 0;
}

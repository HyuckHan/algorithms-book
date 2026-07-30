#include "graph.h"
#include <stdio.h>

static void print_ints(const char *label, const int *a, size_t n) {
    printf("%s:", label);
    for (size_t i = 0; i < n; i++) printf(" %d", a[i]);
    printf("\n");
}
static void print_szs(const char *label, const size_t *a, size_t n) {
    printf("%s:", label);
    for (size_t i = 0; i < n; i++) printf(" %zu", a[i]);
    printf("\n");
}
static void print_ptrdiffs(const char *label, const ptrdiff_t *a, size_t n) {
    printf("%s:", label);
    for (size_t i = 0; i < n; i++) printf(" %td", a[i]);
    printf("\n");
}

int main(void) {
    Graph *g = graph_create(8, false);
    size_t edges[][2] = {{0,1},{0,2},{0,3},{1,4},{2,4},{2,5},{3,6},{4,7},{6,7}};
    for (size_t i = 0; i < 9; i++) graph_add_edge(g, edges[i][0], edges[i][1], 1);

    int dist[8]; ptrdiff_t parent[8]; size_t order[8];
    graph_bfs(g, 0, dist, parent, order);
    print_szs("bfs order", order, 8);
    print_ints("bfs dist", dist, 8);
    print_ptrdiffs("bfs parent", parent, 8);

    size_t discover[8], finish[8]; ptrdiff_t dfs_parent[8];
    graph_dfs(g, discover, finish, dfs_parent);
    print_szs("dfs discover", discover, 8);
    print_szs("dfs finish", finish, 8);
    print_ptrdiffs("dfs parent", dfs_parent, 8);

    graph_destroy(g);
    return 0;
}

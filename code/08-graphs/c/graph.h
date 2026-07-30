#ifndef LECTURE08_GRAPH_H
#define LECTURE08_GRAPH_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define GRAPH_INF (INT64_MAX / 4)
typedef struct { size_t to; int64_t weight; } Edge;
typedef struct { Edge *data; size_t size, capacity; } EdgeVec;
typedef struct { size_t n; bool directed; EdgeVec *adj; } Graph;
typedef struct { size_t u, v; int64_t weight; } MstEdge;
typedef struct { MstEdge *edges; size_t count; int64_t weight; bool connected; } MstResult;

Graph *graph_create(size_t n, bool directed);
bool graph_add_edge(Graph *g, size_t u, size_t v, int64_t weight);
bool graph_weight(const Graph *g, size_t u, size_t v, int64_t *out);
bool graph_validate(const Graph *g);
void graph_destroy(Graph *g);

bool graph_bfs(const Graph *g, size_t s, int *dist, ptrdiff_t *parent, size_t *order);
bool graph_dfs(const Graph *g, size_t *discover, size_t *finish, ptrdiff_t *parent);
bool graph_dfs_iterative(const Graph *g, size_t s, size_t *visit_order);
bool graph_topological_kahn(const Graph *g, size_t *order);
bool graph_topological_dfs(const Graph *g, size_t *order);

typedef struct { size_t *parent; unsigned char *rank; size_t n; } DisjointSet;
bool dsu_init(DisjointSet *d, size_t n);
size_t dsu_find(DisjointSet *d, size_t x);
bool dsu_union(DisjointSet *d, size_t a, size_t b);
void dsu_destroy(DisjointSet *d);

bool graph_prim(const Graph *g, size_t root, MstResult *out);
bool graph_kruskal(const Graph *g, MstResult *out);
void mst_result_destroy(MstResult *r);

bool graph_dijkstra(const Graph *g, size_t s, int64_t *dist, ptrdiff_t *parent);
bool graph_bellman_ford(const Graph *g, size_t s, int64_t *dist,
                        ptrdiff_t *parent, bool *negative_cycle);
bool graph_reconstruct_path(size_t n, size_t s, size_t target,
                            const ptrdiff_t *parent, size_t *path, size_t *length);
bool graph_dag_shortest_paths(const Graph *g, size_t s, int64_t *dist, ptrdiff_t *parent);
#endif

// Reused verbatim from lecture-notes/code/lecture08/c/mst.c.
#include "graph.h"
#include <stdlib.h>
#include <limits.h>

static int edge_cmp(const void *a, const void *b) {
    const MstEdge *x = a, *y = b;
    if (x->weight != y->weight) return x->weight < y->weight ? -1 : 1;
    if (x->u != y->u) return x->u < y->u ? -1 : 1;
    return x->v == y->v ? 0 : (x->v < y->v ? -1 : 1);
}
void mst_result_destroy(MstResult *r) { if (r) { free(r->edges); *r = (MstResult){0}; } }

// snippet:kruskal:start
bool graph_kruskal(const Graph *g, MstResult *out) {
    if (!g || !out || g->directed) return false;
    size_t m = 0;
    for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) if (u < g->adj[u].data[i].to) m++;
    MstEdge *all = malloc((m ? m : 1) * sizeof(*all));
    MstEdge *sel = malloc((g->n ? g->n - 1 : 0) * sizeof(*sel) + sizeof(*sel));
    DisjointSet d = {0};
    if (!all || !sel || !dsu_init(&d, g->n)) { free(all); free(sel); dsu_destroy(&d); return false; }
    size_t k = 0;
    for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) {
        Edge e = g->adj[u].data[i]; if (u < e.to) all[k++] = (MstEdge){u,e.to,e.weight};
    }
    qsort(all, m, sizeof(*all), edge_cmp);
    size_t count = 0; int64_t total = 0;
    for (size_t i = 0; i < m && count + 1 < g->n; i++) if (dsu_union(&d, all[i].u, all[i].v)) {
        sel[count++] = all[i]; total += all[i].weight;
    }
    free(all); dsu_destroy(&d);
    *out = (MstResult){sel,count,total,count + 1 == g->n || g->n == 0}; return true;
}
// snippet:kruskal:end

// snippet:prim:start
bool graph_prim(const Graph *g, size_t root, MstResult *out) {
    if (!g || !out || g->directed || root >= g->n) return false;
    int64_t *key = malloc(g->n * sizeof(*key)); ptrdiff_t *p = malloc(g->n * sizeof(*p));
    bool *in = calloc(g->n, sizeof(*in)); MstEdge *sel = malloc(g->n * sizeof(*sel));
    if (!key || !p || !in || !sel) { free(key); free(p); free(in); free(sel); return false; }
    for (size_t i = 0; i < g->n; i++) { key[i] = GRAPH_INF; p[i] = -1; } key[root] = 0;
    size_t count = 0; int64_t total = 0;
    for (size_t step = 0; step < g->n; step++) {
        size_t u = g->n;
        for (size_t v = 0; v < g->n; v++) if (!in[v] && (u == g->n || key[v] < key[u])) u = v;
        if (u == g->n || key[u] == GRAPH_INF) break;
        in[u] = true;
        if (p[u] >= 0) { sel[count++] = (MstEdge){(size_t)p[u],u,key[u]}; total += key[u]; }
        for (size_t i = 0; i < g->adj[u].size; i++) {
            Edge e = g->adj[u].data[i];
            if (!in[e.to] && e.weight < key[e.to]) { key[e.to] = e.weight; p[e.to] = (ptrdiff_t)u; }
        }
    }
    free(key); free(p); free(in); *out = (MstResult){sel,count,total,count + 1 == g->n}; return true;
}
// snippet:prim:end

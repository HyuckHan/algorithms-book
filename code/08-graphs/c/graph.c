// Reused verbatim from lecture-notes/code/lecture08/c/graph.c. Shared by
// every algorithm demo in this chapter, so it carries no single snippet
// marker of its own -- each algorithm's snippet is the function that uses it.
#include "graph.h"
#include <stdlib.h>

static bool reserve(EdgeVec *v, size_t need) {
    if (need <= v->capacity) return true;
    size_t cap = v->capacity ? v->capacity * 2 : 4;
    if (cap < need || cap > SIZE_MAX / sizeof(Edge)) return false;
    Edge *p = realloc(v->data, cap * sizeof(*p));
    if (!p) return false;
    v->data = p; v->capacity = cap; return true;
}
static bool put_arc(Graph *g, size_t u, size_t v, int64_t w) {
    EdgeVec *a = &g->adj[u];
    for (size_t i = 0; i < a->size; i++) if (a->data[i].to == v) {
        a->data[i].weight = w; return true; /* duplicate policy: update */
    }
    if (!reserve(a, a->size + 1)) return false;
    size_t i = a->size++;
    while (i && a->data[i - 1].to > v) { a->data[i] = a->data[i - 1]; i--; }
    a->data[i] = (Edge){v, w}; return true;
}
Graph *graph_create(size_t n, bool directed) {
    if (n && n > SIZE_MAX / sizeof(EdgeVec)) return NULL;
    Graph *g = calloc(1, sizeof(*g));
    if (!g) return NULL;
    g->adj = calloc(n ? n : 1, sizeof(*g->adj));
    if (!g->adj) { free(g); return NULL; }
    g->n = n; g->directed = directed; return g;
}
bool graph_add_edge(Graph *g, size_t u, size_t v, int64_t w) {
    if (!g || u >= g->n || v >= g->n) return false;
    int64_t old = 0; bool had = graph_weight(g, u, v, &old);
    if (!put_arc(g, u, v, w)) return false;
    if (!g->directed && u != v && !put_arc(g, v, u, w)) {
        if (had) (void)put_arc(g, u, v, old);
        return false;
    }
    return true;
}
bool graph_weight(const Graph *g, size_t u, size_t v, int64_t *out) {
    if (!g || u >= g->n || v >= g->n) return false;
    for (size_t i = 0; i < g->adj[u].size; i++) if (g->adj[u].data[i].to == v) {
        if (out) *out = g->adj[u].data[i].weight;
        return true;
    }
    return false;
}
bool graph_validate(const Graph *g) {
    if (!g) return false;
    for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) {
        Edge e = g->adj[u].data[i];
        if (e.to >= g->n || (i && g->adj[u].data[i-1].to >= e.to)) return false;
        int64_t w = 0;
        if (!g->directed && (!graph_weight(g, e.to, u, &w) || w != e.weight)) return false;
    }
    return true;
}
void graph_destroy(Graph *g) {
    if (!g) return;
    for (size_t i = 0; i < g->n; i++) free(g->adj[i].data);
    free(g->adj); free(g);
}

// Reused verbatim from lecture-notes/code/lecture08/c/shortest_paths.c.
#include "graph.h"
#include <stdlib.h>

static bool add_safe(int64_t a, int64_t b, int64_t *out) {
    if (a == GRAPH_INF) return false;
    if ((b > 0 && a > GRAPH_INF - b) || (b < 0 && a < -GRAPH_INF - b)) return false;
    *out = a + b; return true;
}

// snippet:dijkstra:start
bool graph_dijkstra(const Graph *g, size_t s, int64_t *d, ptrdiff_t *p) {
    if (!g || s >= g->n || !d || !p) return false;
    for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) if (g->adj[u].data[i].weight < 0) return false;
    bool *done = calloc(g->n ? g->n : 1, sizeof(*done)); if (!done) return false;
    for (size_t i = 0; i < g->n; i++) { d[i] = GRAPH_INF; p[i] = -1; } d[s] = 0;
    for (size_t step = 0; step < g->n; step++) {
        size_t u = g->n;
        for (size_t v = 0; v < g->n; v++) if (!done[v] && (u == g->n || d[v] < d[u])) u = v;
        if (u == g->n || d[u] == GRAPH_INF) break;
        done[u] = true;
        for (size_t i = 0; i < g->adj[u].size; i++) {
            Edge e = g->adj[u].data[i]; int64_t cand;
            if (!done[e.to] && add_safe(d[u], e.weight, &cand) && cand < d[e.to]) { d[e.to] = cand; p[e.to] = (ptrdiff_t)u; }
        }
    }
    free(done); return true;
}
// snippet:dijkstra:end

// snippet:bellman-ford:start
bool graph_bellman_ford(const Graph *g, size_t s, int64_t *d, ptrdiff_t *p, bool *neg) {
    if (!g || s >= g->n || !d || !p || !neg) return false;
    for (size_t i = 0; i < g->n; i++) { d[i] = GRAPH_INF; p[i] = -1; } d[s] = 0; *neg = false;
    for (size_t pass = 1; pass < g->n; pass++) {
        bool changed = false;
        for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) {
            Edge e = g->adj[u].data[i]; int64_t cand;
            if (add_safe(d[u], e.weight, &cand) && cand < d[e.to]) { d[e.to] = cand; p[e.to] = (ptrdiff_t)u; changed = true; }
        }
        if (!changed) break;
    }
    for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) {
        Edge e = g->adj[u].data[i]; int64_t cand;
        if (add_safe(d[u], e.weight, &cand) && cand < d[e.to]) { *neg = true; return true; }
    }
    return true;
}
// snippet:bellman-ford:end

// snippet:reconstruct-path:start
bool graph_reconstruct_path(size_t n, size_t s, size_t target, const ptrdiff_t *p, size_t *path, size_t *len) {
    if (!p || !path || !len || s >= n || target >= n) return false;
    size_t used = 0, v = target;
    while (true) {
        if (used >= n) return false;
        path[used++] = v;
        if (v == s) break;
        if (p[v] < 0) return false;
        v = (size_t)p[v];
    }
    for (size_t i = 0; i < used / 2; i++) { size_t t = path[i]; path[i] = path[used-1-i]; path[used-1-i] = t; }
    *len = used; return true;
}
// snippet:reconstruct-path:end

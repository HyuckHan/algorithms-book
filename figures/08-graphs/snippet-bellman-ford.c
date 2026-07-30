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

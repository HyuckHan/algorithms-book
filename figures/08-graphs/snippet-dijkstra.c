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

static void visit(const Graph *g, size_t u, unsigned char *color, size_t *d,
                  size_t *f, ptrdiff_t *p, size_t *time) {
    color[u] = 1; d[u] = ++*time;
    for (size_t i = 0; i < g->adj[u].size; i++) {
        size_t v = g->adj[u].data[i].to;
        if (!color[v]) { p[v] = (ptrdiff_t)u; visit(g, v, color, d, f, p, time); }
    }
    color[u] = 2; f[u] = ++*time;
}
bool graph_dfs(const Graph *g, size_t *d, size_t *f, ptrdiff_t *p) {
    if (!g || !d || !f || !p) return false;
    unsigned char *color = calloc(g->n ? g->n : 1, 1);
    if (!color) return false;
    for (size_t i = 0; i < g->n; i++) p[i] = -1;
    size_t time = 0;
    for (size_t u = 0; u < g->n; u++) if (!color[u]) visit(g, u, color, d, f, p, &time);
    free(color); return true;
}

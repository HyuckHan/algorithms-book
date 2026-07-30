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

bool graph_bfs(const Graph *g, size_t s, int *dist, ptrdiff_t *parent, size_t *order) {
    if (!g || s >= g->n || !dist || !parent || !order) return false;
    unsigned char *color = calloc(g->n ? g->n : 1, 1);
    size_t *q = malloc((g->n ? g->n : 1) * sizeof(*q));
    if (!color || !q) { free(color); free(q); return false; }
    for (size_t i = 0; i < g->n; i++) { dist[i] = -1; parent[i] = -1; }
    size_t head = 0, tail = 0, used = 0;
    color[s] = 1; dist[s] = 0; q[tail++] = s;
    while (head < tail) {
        size_t u = q[head++]; order[used++] = u;
        for (size_t i = 0; i < g->adj[u].size; i++) {
            size_t v = g->adj[u].data[i].to;
            if (!color[v]) { color[v] = 1; dist[v] = dist[u] + 1; parent[v] = (ptrdiff_t)u; q[tail++] = v; }
        }
        color[u] = 2;
    }
    free(color); free(q); return true;
}

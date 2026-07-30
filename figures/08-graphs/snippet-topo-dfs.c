enum { WHITE = 0, GRAY = 1, BLACK = 2 };

static bool topo_visit(const Graph *g, size_t u, unsigned char *color, size_t *finish, size_t *count) {
    color[u] = GRAY;
    for (size_t i = 0; i < g->adj[u].size; i++) {
        size_t v = g->adj[u].data[i].to;
        if (color[v] == GRAY) return false;
        if (color[v] == WHITE && !topo_visit(g, v, color, finish, count)) return false;
    }
    color[u] = BLACK;
    finish[(*count)++] = u;
    return true;
}
bool graph_topological_dfs(const Graph *g, size_t *order) {
    if (!g || !order || !g->directed) return false;
    unsigned char *color = calloc(g->n ? g->n : 1, 1);
    if (!color) return false;
    size_t count = 0;
    bool ok = true;
    for (size_t u = 0; ok && u < g->n; u++)
        if (color[u] == WHITE) ok = topo_visit(g, u, color, order, &count);
    free(color);
    if (!ok) return false;
    for (size_t i = 0; i < g->n / 2; i++) { size_t t = order[i]; order[i] = order[g->n-1-i]; order[g->n-1-i] = t; }
    return true;
}

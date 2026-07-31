static bool safe(const unsigned char *adj, size_t n, size_t v, int color,
                 const int *colors) {
    size_t u;
    for (u = 0; u < v; u++)
        if (adj[v * n + u] && colors[u] == color) return false;
    return true;
}

static bool dfs(const unsigned char *adj, size_t n, int m, size_t v, int *colors) {
    int c;
    if (v == n) return true;
    for (c = 1; c <= m; c++) {
        if (safe(adj, n, v, c, colors)) {
            colors[v] = c;
            if (dfs(adj, n, m, v + 1, colors)) return true;
            colors[v] = 0;
        }
    }
    return false;
}

ss_status ss_color_graph(const unsigned char *adjacency, size_t n, int m,
                         int *colors) {
    size_t i;
    if (adjacency == NULL || colors == NULL || m < 0) return SS_INVALID;
    for (i = 0; i < n; i++) colors[i] = 0;
    return dfs(adjacency, n, m, 0, colors) ? SS_OK : SS_NO_SOLUTION;
}

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

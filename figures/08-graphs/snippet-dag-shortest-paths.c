bool graph_dag_shortest_paths(const Graph *g, size_t s, int64_t *dist, ptrdiff_t *parent) {
    if (!g || s >= g->n || !dist || !parent) return false;
    size_t *order = malloc(g->n * sizeof(*order));
    if (!order || !graph_topological_kahn(g, order)) { free(order); return false; }
    for (size_t i = 0; i < g->n; i++) { dist[i] = GRAPH_INF; parent[i] = -1; }
    dist[s] = 0;
    for (size_t i = 0; i < g->n; i++) {
        size_t u = order[i];
        if (dist[u] == GRAPH_INF) continue;
        for (size_t j = 0; j < g->adj[u].size; j++) {
            Edge e = g->adj[u].data[j];
            int64_t cand = dist[u] + e.weight;
            if (cand < dist[e.to]) { dist[e.to] = cand; parent[e.to] = (ptrdiff_t)u; }
        }
    }
    free(order); return true;
}

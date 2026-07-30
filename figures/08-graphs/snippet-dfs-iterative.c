bool graph_dfs_iterative(const Graph *g, size_t s, size_t *visit_order) {
    if (!g || s >= g->n || !visit_order) return false;
    bool *discovered = calloc(g->n, sizeof(*discovered));
    size_t *stack = malloc(g->n * sizeof(*stack));
    if (!discovered || !stack) { free(discovered); free(stack); return false; }
    size_t top = 0, used = 0;
    stack[top++] = s; discovered[s] = true;
    while (top) {
        size_t u = stack[--top];
        visit_order[used++] = u;
        for (size_t i = g->adj[u].size; i-- > 0; ) {
            size_t v = g->adj[u].data[i].to;
            if (!discovered[v]) { discovered[v] = true; stack[top++] = v; }
        }
    }
    free(discovered); free(stack); return true;
}

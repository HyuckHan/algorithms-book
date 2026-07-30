#include "graph.h"
#include <stdlib.h>

// Reused verbatim from lecture-notes/code/lecture08/c/topological_sort.c.
// snippet:topo-kahn:start
bool graph_topological_kahn(const Graph *g, size_t *order) {
    /* This compact implementation scans for the smallest zero-indegree
       vertex, so it is O(V^2 + E). A queue/stack Kahn implementation is
       Theta(V + E); a binary min-heap implementation is O(E + V log V). */
    if (!g || !order || !g->directed) return false;
    size_t *in = calloc(g->n ? g->n : 1, sizeof(*in));
    bool *used = calloc(g->n ? g->n : 1, sizeof(*used));
    if (!in || !used) { free(in); free(used); return false; }
    for (size_t u = 0; u < g->n; u++) for (size_t i = 0; i < g->adj[u].size; i++) in[g->adj[u].data[i].to]++;
    size_t count = 0;
    while (count < g->n) {
        size_t u = g->n;
        for (size_t v = 0; v < g->n; v++) if (!used[v] && in[v] == 0) { u = v; break; }
        if (u == g->n) break;
        used[u] = true; order[count++] = u;
        for (size_t i = 0; i < g->adj[u].size; i++) in[g->adj[u].data[i].to]--;
    }
    free(in); free(used); return count == g->n;
}
// snippet:topo-kahn:end

// New: DFS-based topological sort (only Kahn exists in the canonical C
// source) -- 3-color GRAY-back-edge cycle detection, matching HasCycleDFS,
// plus finish-order append and an outer reverse.
// snippet:topo-dfs:start
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
// snippet:topo-dfs:end

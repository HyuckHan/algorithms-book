// Reused verbatim from lecture-notes/code/lecture08/c/bfs_dfs.c.
#include "graph.h"
#include <stdlib.h>
#include <string.h>

// snippet:bfs:start
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
// snippet:bfs:end

// snippet:dfs:start
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
// snippet:dfs:end

/* lecture-notes/code/lecture10/c/a_star_grid.c와 같은 정책(4-neighbor
 * unit-cost grid, Manhattan heuristic, stale-g-snapshot 검사, permanent
 * CLOSED). */
#include "state_space_search.h"
#include <limits.h>
#include <stdlib.h>

// snippet:a-star:start
typedef struct { size_t cell; int64_t g; int64_t f; } entry;

static int less(entry a, entry b) {
    if (a.f != b.f) return a.f < b.f;
    if (a.g != b.g) return a.g < b.g;
    return a.cell < b.cell;
}
static void push(entry *h, size_t *n, entry x) {
    size_t i = (*n)++;
    while (i > 0U) {
        size_t p = (i - 1U) / 2U;
        if (!less(x, h[p])) break;
        h[i] = h[p]; i = p;
    }
    h[i] = x;
}
static entry pop(entry *h, size_t *n) {
    entry top = h[0], x = h[--(*n)];
    size_t i = 0U;
    while (2U * i + 1U < *n) {
        size_t c = 2U * i + 1U;
        if (c + 1U < *n && less(h[c + 1U], h[c])) c++;
        if (!less(h[c], x)) break;
        h[i] = h[c]; i = c;
    }
    if (*n != 0U) h[i] = x;
    return top;
}
static int64_t heuristic(size_t cell, size_t goal, size_t cols, bool zero) {
    size_t r1 = cell / cols, c1 = cell % cols;
    size_t r2 = goal / cols, c2 = goal % cols;
    if (zero) return 0;
    return (int64_t)(r1 > r2 ? r1-r2 : r2-r1) +
           (int64_t)(c1 > c2 ? c1-c2 : c2-c1);
}

ss_status ss_astar_grid(const unsigned char *blocked, size_t rows, size_t cols,
                        size_t start, size_t goal, bool zero_heuristic,
                        int64_t *cost, ss_metrics *metrics) {
    size_t cells, heap_cap, heap_size = 0U, i;
    int64_t *g;
    unsigned char *closed;
    entry *heap;
    static const int dr[4] = {-1, 0, 0, 1};
    static const int dc[4] = {0, -1, 1, 0};
    ss_metrics local = {0U,0U,0U,0U};
    if (blocked == NULL || cost == NULL || metrics == NULL || rows == 0U ||
        cols == 0U || rows > SIZE_MAX / cols) return SS_INVALID;
    cells = rows * cols;
    if (start >= cells || goal >= cells || blocked[start] || blocked[goal] ||
        cells > (SIZE_MAX - 1U) / 4U) return SS_INVALID;
    heap_cap = 4U * cells + 1U;
    g = malloc(cells * sizeof(*g));
    closed = calloc(cells, sizeof(*closed));
    heap = malloc(heap_cap * sizeof(*heap));
    if (g == NULL || closed == NULL || heap == NULL) {
        free(g); free(closed); free(heap); return SS_NO_MEMORY;
    }
    for (i = 0; i < cells; i++) g[i] = INT64_MAX;
    g[start] = 0;
    push(heap,&heap_size,(entry){start,0,heuristic(start,goal,cols,zero_heuristic)});
    *cost = INT64_MAX;
    while (heap_size != 0U) {
        entry e = pop(heap,&heap_size);
        size_t r = e.cell / cols, c = e.cell % cols;
        int d;
        if (e.g != g[e.cell]) continue;
        if (closed[e.cell] != 0U) continue;
        closed[e.cell] = 1U;
        local.expanded++;
        if (heap_size > local.max_frontier) local.max_frontier = heap_size;
        if (e.cell == goal) { *cost = e.g; break; }
        for (d = 0; d < 4; d++) {
            int64_t nr = (int64_t)r + dr[d], nc = (int64_t)c + dc[d];
            size_t v;
            int64_t ng;
            if (nr < 0 || nc < 0 || nr >= (int64_t)rows || nc >= (int64_t)cols) continue;
            v = (size_t)nr * cols + (size_t)nc;
            if (blocked[v] || closed[v] != 0U) continue;
            ng = e.g + 1;
            if (ng < g[v]) {
                g[v] = ng;
                push(heap,&heap_size,(entry){v,ng,ng+heuristic(v,goal,cols,zero_heuristic)});
            }
        }
    }
    free(g); free(closed); free(heap); *metrics = local;
    return *cost == INT64_MAX ? SS_NO_SOLUTION : SS_OK;
}
// snippet:a-star:end

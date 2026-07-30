#include "graph.h"
#include <stdlib.h>

bool dsu_init(DisjointSet *d, size_t n) {
    if (!d || n > SIZE_MAX / sizeof(size_t)) return false;
    d->parent = malloc((n ? n : 1) * sizeof(*d->parent));
    d->rank = calloc(n ? n : 1, sizeof(*d->rank)); d->n = n;
    if (!d->parent || !d->rank) { dsu_destroy(d); return false; }
    for (size_t i = 0; i < n; i++) d->parent[i] = i;
    return true;
}
size_t dsu_find(DisjointSet *d, size_t x) {
    if (d->parent[x] != x) d->parent[x] = dsu_find(d, d->parent[x]);
    return d->parent[x];
}
bool dsu_union(DisjointSet *d, size_t a, size_t b) {
    size_t x = dsu_find(d, a), y = dsu_find(d, b);
    if (x == y) return false;
    if (d->rank[x] < d->rank[y]) { size_t t = x; x = y; y = t; }
    d->parent[y] = x;
    if (d->rank[x] == d->rank[y]) d->rank[x]++;
    return true;
}
void dsu_destroy(DisjointSet *d) {
    if (!d) return;
    free(d->parent);
    free(d->rank);
    d->parent = NULL; d->rank = NULL; d->n = 0;
}

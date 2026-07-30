bool graph_reconstruct_path(size_t n, size_t s, size_t target, const ptrdiff_t *p, size_t *path, size_t *len) {
    if (!p || !path || !len || s >= n || target >= n) return false;
    size_t used = 0, v = target;
    while (true) {
        if (used >= n) return false;
        path[used++] = v;
        if (v == s) break;
        if (p[v] < 0) return false;
        v = (size_t)p[v];
    }
    for (size_t i = 0; i < used / 2; i++) { size_t t = path[i]; path[i] = path[used-1-i]; path[used-1-i] = t; }
    *len = used; return true;
}

static ss_status place(size_t row, size_t n, unsigned char *col,
                       unsigned char *d1, unsigned char *d2,
                       uint64_t *count, ss_metrics *m) {
    size_t c;
    m->expanded++;
    if (row > m->max_depth) m->max_depth = row;
    if (row == n) {
        if (*count == UINT64_MAX) return SS_OVERFLOW;
        (*count)++;
        return SS_OK;
    }
    for (c = 0; c < n; c++) {
        size_t a = row + (n - 1U) - c;
        size_t b = row + c;
        ss_status s;
        if (col[c] != 0U || d1[a] != 0U || d2[b] != 0U) {
            m->pruned++;
            continue;
        }
        col[c] = d1[a] = d2[b] = 1U;
        s = place(row + 1U, n, col, d1, d2, count, m);
        col[c] = d1[a] = d2[b] = 0U;
        if (s != SS_OK) return s;
    }
    return SS_OK;
}

ss_status ss_n_queens_count(size_t n, uint64_t *count, ss_metrics *metrics) {
    unsigned char *storage;
    size_t diag;
    ss_metrics local = {0U, 0U, 0U, 0U};
    if (count == NULL || metrics == NULL || n > 30U) return SS_INVALID;
    *count = 0U;
    if (n == 0U) { *count = 1U; *metrics = local; return SS_OK; }
    diag = 2U * n - 1U;
    if (n > SIZE_MAX - 2U * diag) return SS_OVERFLOW;
    storage = calloc(n + 2U * diag, sizeof(*storage));
    if (storage == NULL) return SS_NO_MEMORY;
    {
        ss_status s = place(0U, n, storage, storage + n, storage + n + diag,
                            count, &local);
        free(storage);
        *metrics = local;
        return s;
    }
}

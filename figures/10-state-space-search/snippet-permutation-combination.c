static ss_status permute(size_t n, size_t k, size_t depth, unsigned char *used,
                         uint64_t *count, ss_metrics *m) {
    size_t v;
    m->expanded++;
    if (depth > m->max_depth) m->max_depth = depth;
    if (depth == k) {
        if (*count == UINT64_MAX) return SS_OVERFLOW;
        (*count)++;
        return SS_OK;
    }
    for (v = 0; v < n; v++) {
        ss_status s;
        if (used[v] != 0U) continue;
        used[v] = 1U;
        s = permute(n, k, depth + 1U, used, count, m);
        used[v] = 0U;
        if (s != SS_OK) return s;
    }
    return SS_OK;
}

ss_status ss_permutation_count(size_t n, size_t k, uint64_t *count,
                               ss_metrics *metrics) {
    unsigned char *used;
    ss_metrics local = {0U, 0U, 0U, 0U};
    if (count == NULL || metrics == NULL || k > n) return SS_INVALID;
    *count = 0U;
    used = n == 0U ? NULL : calloc(n, sizeof(*used));
    if (n != 0U && used == NULL) return SS_NO_MEMORY;
    {
        ss_status s = permute(n, k, 0U, used, count, &local);
        free(used);
        *metrics = local;
        return s;
    }
}

/* New in this book's port: the original C file only ports ChoosePermutation,
 * not ChooseCombination -- added here with the same start-index technique
 * as PermutationGenerator.combinations() (Java) so the demo runs a real
 * combination-counting recursion instead of deriving C(n,k) arithmetically
 * from P(n,k). */
static ss_status combine(size_t n, size_t k, size_t start, size_t depth,
                         uint64_t *count, ss_metrics *m) {
    size_t value;
    m->expanded++;
    if (depth > m->max_depth) m->max_depth = depth;
    if (depth == k) {
        if (*count == UINT64_MAX) return SS_OVERFLOW;
        (*count)++;
        return SS_OK;
    }
    for (value = start; value <= n - (k - depth); value++) {
        ss_status s = combine(n, k, value + 1U, depth + 1U, count, m);
        if (s != SS_OK) return s;
    }
    return SS_OK;
}

ss_status ss_combination_count(size_t n, size_t k, uint64_t *count,
                               ss_metrics *metrics) {
    ss_metrics local = {0U, 0U, 0U, 0U};
    if (count == NULL || metrics == NULL || k > n) return SS_INVALID;
    *count = 0U;
    {
        ss_status s = combine(n, k, 0U, 0U, count, &local);
        *metrics = local;
        return s;
    }
}

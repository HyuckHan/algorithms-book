/* lecture-notes/code/lecture10/c/subset_sum.c와 같은 정책(양의 weight 전제
 * 아래 두 sound pruning: sum>target, sum+remaining<target). */
#include "state_space_search.h"
#include <limits.h>

// snippet:subset-sum:start
static ss_status add_i64(int64_t a, int64_t b, int64_t *out) {
    if ((b > 0 && a > INT64_MAX - b) || (b < 0 && a < INT64_MIN - b))
        return SS_OVERFLOW;
    *out = a + b;
    return SS_OK;
}

static ss_status subset(const int64_t *w, size_t n, int64_t target, size_t i,
                        int64_t sum, int64_t remaining, uint64_t mask,
                        uint64_t *masks, size_t capacity, size_t *count,
                        bool pruning, ss_metrics *m) {
    int64_t next;
    ss_status s;
    m->expanded++;
    if (i > m->max_depth) m->max_depth = i;
    if (sum == target) {
        if (*count < capacity) masks[*count] = mask;
        (*count)++;
        return SS_OK;
    }
    if (i == n) return SS_OK;
    if (pruning && (sum > target ||
                    (remaining < target && sum < target - remaining))) {
        m->pruned++;
        return SS_OK;
    }
    s = add_i64(sum, w[i], &next);
    if (s != SS_OK) return s;
    s = subset(w, n, target, i + 1U, next, remaining - w[i],
               mask | (UINT64_C(1) << i), masks, capacity, count, pruning, m);
    if (s != SS_OK) return s;
    return subset(w, n, target, i + 1U, sum, remaining - w[i],
                  mask, masks, capacity, count, pruning, m);
}

ss_status ss_subset_sum_masks(const int64_t *weights, size_t n, int64_t target,
                              uint64_t *masks, size_t capacity,
                              size_t *solution_count, bool pruning,
                              ss_metrics *metrics) {
    size_t i;
    int64_t remaining = 0;
    ss_metrics local = {0U, 0U, 0U, 0U};
    if (weights == NULL || masks == NULL || solution_count == NULL ||
        metrics == NULL || target < 0 || n > 63U) return SS_INVALID;
    for (i = 0; i < n; i++) {
        if (weights[i] <= 0) return SS_INVALID;
        if (add_i64(remaining, weights[i], &remaining) != SS_OK) return SS_OVERFLOW;
    }
    *solution_count = 0U;
    {
        ss_status s = subset(weights, n, target, 0U, 0, remaining, 0U,
                             masks, capacity, solution_count, pruning, &local);
        *metrics = local;
        return *solution_count > capacity && s == SS_OK ? SS_OVERFLOW : s;
    }
}
// snippet:subset-sum:end

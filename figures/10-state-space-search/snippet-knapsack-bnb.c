typedef struct {
    size_t level;
    int64_t weight;
    int64_t profit;
    long double bound;
    uint64_t mask;
} node;

static int ratio_before(const ss_item *a, const ss_item *b) {
    long double ra = (long double)a->profit / (long double)a->weight;
    long double rb = (long double)b->profit / (long double)b->weight;
    return ra > rb;
}

static long double upper(const ss_item *a, size_t n, int64_t cap,
                         size_t level, int64_t weight, int64_t profit) {
    size_t i;
    int64_t remain = cap - weight;
    long double value = (long double)profit;
    if (remain < 0) return -1.0L;
    for (i = level; i < n && remain > 0; i++) {
        if (a[i].weight <= remain) {
            remain -= a[i].weight;
            value += (long double)a[i].profit;
        } else {
            value += (long double)a[i].profit * (long double)remain /
                     (long double)a[i].weight;
            break;
        }
    }
    return value;
}

static void heap_push(node *h, size_t *size, node x) {
    size_t i = (*size)++;
    while (i > 0U) {
        size_t p = (i - 1U) / 2U;
        if (h[p].bound >= x.bound) break;
        h[i] = h[p]; i = p;
    }
    h[i] = x;
}

static node heap_pop(node *h, size_t *size) {
    node top = h[0], x = h[--(*size)];
    size_t i = 0U;
    while (2U * i + 1U < *size) {
        size_t c = 2U * i + 1U;
        if (c + 1U < *size && h[c + 1U].bound > h[c].bound) c++;
        if (h[c].bound <= x.bound) break;
        h[i] = h[c]; i = c;
    }
    if (*size != 0U) h[i] = x;
    return top;
}

static ss_status ensure_heap(node **heap, size_t *capacity, size_t need) {
    node *grown;
    size_t next;
    if (need <= *capacity) return SS_OK;
    if (*capacity > SIZE_MAX / 2U) return SS_OVERFLOW;
    next = *capacity * 2U;
    if (next < need || next > SIZE_MAX / sizeof(**heap)) return SS_OVERFLOW;
    grown = realloc(*heap, next * sizeof(**heap));
    if (grown == NULL) return SS_NO_MEMORY;
    *heap = grown;
    *capacity = next;
    return SS_OK;
}

ss_status ss_knapsack_bnb(const ss_item *input, size_t n, int64_t capacity,
                          ss_knapsack_result *result) {
    ss_item *a;
    node *heap;
    size_t i, j, size = 0U, heap_cap;
    if (input == NULL || result == NULL || capacity < 0 || n > 63U) return SS_INVALID;
    if (n > (SIZE_MAX - 1U) / 2U) return SS_OVERFLOW;
    heap_cap = 2U * n + 1U;
    a = n == 0U ? NULL : malloc(n * sizeof(*a));
    heap = malloc(heap_cap * sizeof(*heap));
    if ((n != 0U && a == NULL) || heap == NULL) { free(a); free(heap); return SS_NO_MEMORY; }
    for (i = 0; i < n; i++) {
        if (input[i].weight <= 0 || input[i].profit < 0) { free(a); free(heap); return SS_INVALID; }
        a[i] = input[i];
    }
    for (i = 1; i < n; i++) {
        ss_item x = a[i]; j = i;
        while (j > 0U && ratio_before(&x, &a[j - 1U])) { a[j] = a[j - 1U]; j--; }
        a[j] = x;
    }
    *result = (ss_knapsack_result){0, 0, 0U, {0U,0U,0U,0U}};
    {
        node root = {0U,0,0,upper(a,n,capacity,0U,0,0),0U};
        heap_push(heap,&size,root);
    }
    while (size != 0U) {
        node p = heap_pop(heap,&size);
        node c;
        if (size > result->metrics.max_frontier) result->metrics.max_frontier = size;
        if (p.bound <= (long double)result->profit) { result->metrics.pruned++; continue; }
        result->metrics.expanded++;
        if (p.level == n) continue;
        c = p; c.level++;
        if (a[p.level].weight <= capacity - p.weight &&
            a[p.level].profit <= INT64_MAX - p.profit) {
            c.weight = p.weight + a[p.level].weight;
            c.profit = p.profit + a[p.level].profit;
            c.mask = p.mask | (UINT64_C(1) << p.level);
            if (c.profit > result->profit) {
                result->profit=c.profit;result->weight=c.weight;result->selected_mask=c.mask;
            }
            c.bound=upper(a,n,capacity,c.level,c.weight,c.profit);
            if (c.bound > (long double)result->profit) {
                ss_status s = ensure_heap(&heap, &heap_cap, size + 1U);
                if (s != SS_OK) { free(a); free(heap); return s; }
                heap_push(heap,&size,c);
            } else result->metrics.pruned++;
        }
        c=p;c.level++;c.bound=upper(a,n,capacity,c.level,c.weight,c.profit);
        if (c.bound > (long double)result->profit) {
            ss_status s = ensure_heap(&heap, &heap_cap, size + 1U);
            if (s != SS_OK) { free(a); free(heap); return s; }
            heap_push(heap,&size,c);
        } else result->metrics.pruned++;
    }
    free(a); free(heap); return SS_OK;
}

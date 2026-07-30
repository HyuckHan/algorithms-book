typedef struct Entry {
    int key, value;
    struct Entry *next;
} Entry;

typedef struct {
    Entry **buckets;
    size_t capacity, size;
} ChainTable;

static size_t index_of(int key, size_t capacity) {
    long r = (long)key % (long)capacity;
    return (size_t)(r < 0 ? r + (long)capacity : r);
}

static void chain_init(ChainTable *t, size_t capacity) {
    t->buckets = calloc(capacity, sizeof *t->buckets);
    t->capacity = capacity;
    t->size = 0;
}

static Entry *chain_find(const ChainTable *t, int key) {
    for (Entry *e = t->buckets[index_of(key, t->capacity)]; e; e = e->next)
        if (e->key == key) return e;
    return NULL;
}

static bool chain_get(const ChainTable *t, int key, int *out) {
    Entry *e = chain_find(t, key);
    if (!e) return false;
    *out = e->value;
    return true;
}

static bool chain_put(ChainTable *t, int key, int value, int *old_value) {
    Entry *e = chain_find(t, key);
    if (e) {
        if (old_value) *old_value = e->value;
        e->value = value;
        return true;
    }
    size_t j = index_of(key, t->capacity);
    Entry *n = malloc(sizeof *n);
    *n = (Entry){key, value, t->buckets[j]};
    t->buckets[j] = n;
    t->size++;
    return false;
}

static bool chain_remove(ChainTable *t, int key, int *old_value) {
    size_t j = index_of(key, t->capacity);
    Entry **link = &t->buckets[j];
    while (*link) {
        Entry *e = *link;
        if (e->key == key) {
            *link = e->next;
            if (old_value) *old_value = e->value;
            free(e);
            t->size--;
            return true;
        }
        link = &e->next;
    }
    return false;
}

static int chain_bucket(const ChainTable *t, size_t index, int *out) {
    int n = 0;
    for (Entry *e = t->buckets[index]; e; e = e->next) out[n++] = e->key;
    return n;
}

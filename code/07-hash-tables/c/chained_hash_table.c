#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

/* lecture-notes/code/lecture07/c/chained_hash_table.c와 같은 정책(separate
 * chaining, head insertion, duplicate key는 update)을 따른다. capacity를
 * init 인자로 고정할 수 있게 하고, 데모용 bucket 조회 함수를 추가했다. */

// snippet:chained-hash-table:start
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
// snippet:chained-hash-table:end

static void print_ints(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    ChainTable t;
    chain_init(&t, 7);
    int keys[] = {10, 17, 24};
    for (size_t i = 0; i < sizeof keys / sizeof *keys; i++) chain_put(&t, keys[i], keys[i], NULL);

    int bucket[8], n = chain_bucket(&t, 3, bucket);
    print_ints("bucket3 chain", bucket, n);
    printf("size: %zu\n", t.size);

    int v;
    chain_get(&t, 17, &v);
    printf("get(17): %d\n", v);

    int old = 0;
    chain_put(&t, 17, 170, &old);
    printf("put(17,170) old: %d\n", old);

    chain_get(&t, 17, &v);
    printf("get(17): %d\n", v);

    int removed = 0;
    chain_remove(&t, 17, &removed);
    printf("remove(17): %d\n", removed);

    n = chain_bucket(&t, 3, bucket);
    print_ints("bucket3 chain after remove", bucket, n);
    printf("size after remove: %zu\n", t.size);
    return 0;
}

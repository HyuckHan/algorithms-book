#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

/* lecture-notes/code/lecture07/c/open_address_hash_table.c와 같은 정책(linear
 * probing, EMPTY/OCCUPIED/DELETED tombstone, probing load 기준 resize)을 따르되
 * 데모 출력에 필요한 최소 API로 정리했다. */

// snippet:open-address-hash-table:start
typedef enum { EMPTY, OCCUPIED, DELETED } SlotState;
typedef struct { int key, value; SlotState state; } Slot;
typedef struct {
    Slot *slots;
    size_t capacity, size, tombstones;
} OpenTable;

static size_t index_of(int key, size_t capacity) {
    long r = (long)key % (long)capacity;
    return (size_t)(r < 0 ? r + (long)capacity : r);
}

static void open_init(OpenTable *t, size_t capacity) {
    t->slots = calloc(capacity, sizeof *t->slots);
    t->capacity = capacity;
    t->size = t->tombstones = 0;
}

static bool open_get(const OpenTable *t, int key, int *out) {
    size_t home = index_of(key, t->capacity);
    for (size_t i = 0; i < t->capacity; i++) {
        size_t j = (home + i) % t->capacity;
        if (t->slots[j].state == EMPTY) return false;
        if (t->slots[j].state == OCCUPIED && t->slots[j].key == key) {
            *out = t->slots[j].value;
            return true;
        }
    }
    return false;
}

static void open_reinsert(OpenTable *t, int key, int value) {
    size_t home = index_of(key, t->capacity);
    for (size_t i = 0; i < t->capacity; i++) {
        size_t j = (home + i) % t->capacity;
        if (t->slots[j].state == EMPTY) {
            t->slots[j] = (Slot){key, value, OCCUPIED};
            t->size++;
            return;
        }
    }
}

static void open_resize(OpenTable *t, size_t new_capacity) {
    Slot *old = t->slots;
    size_t old_capacity = t->capacity;
    t->slots = calloc(new_capacity, sizeof *t->slots);
    t->capacity = new_capacity;
    t->size = t->tombstones = 0;
    for (size_t i = 0; i < old_capacity; i++)
        if (old[i].state == OCCUPIED) open_reinsert(t, old[i].key, old[i].value);
    free(old);
}

static bool open_put(OpenTable *t, int key, int value, int *old_value) {
    if ((t->size + t->tombstones + 1) * 100 > t->capacity * 65)
        open_resize(t, t->capacity * 2);

    size_t home = index_of(key, t->capacity);
    long first_deleted = -1;
    for (size_t i = 0; i < t->capacity; i++) {
        size_t j = (home + i) % t->capacity;
        if (t->slots[j].state == OCCUPIED && t->slots[j].key == key) {
            if (old_value) *old_value = t->slots[j].value;
            t->slots[j].value = value;
            return true;
        }
        if (t->slots[j].state == DELETED && first_deleted < 0) first_deleted = (long)j;
        if (t->slots[j].state == EMPTY) {
            size_t target = first_deleted >= 0 ? (size_t)first_deleted : j;
            if (t->slots[target].state == DELETED) t->tombstones--;
            t->slots[target] = (Slot){key, value, OCCUPIED};
            t->size++;
            return false;
        }
    }
    size_t target = (size_t)first_deleted;
    t->slots[target] = (Slot){key, value, OCCUPIED};
    t->size++;
    t->tombstones--;
    return false;
}

static bool open_remove(OpenTable *t, int key, int *old_value) {
    size_t home = index_of(key, t->capacity);
    for (size_t i = 0; i < t->capacity; i++) {
        size_t j = (home + i) % t->capacity;
        if (t->slots[j].state == EMPTY) return false;
        if (t->slots[j].state == OCCUPIED && t->slots[j].key == key) {
            if (old_value) *old_value = t->slots[j].value;
            t->slots[j] = (Slot){0, 0, DELETED};
            t->size--;
            t->tombstones++;
            return true;
        }
    }
    return false;
}
// snippet:open-address-hash-table:end

int main(void) {
    OpenTable t;
    open_init(&t, 8);
    int keys[] = {25, 13, 16, 15, 7, 28, 31, 20, 1, 38};
    for (size_t i = 0; i < sizeof keys / sizeof *keys; i++) open_put(&t, keys[i], keys[i] * 10, NULL);
    printf("size after inserts: %zu\n", t.size);

    int v;
    open_get(&t, 38, &v);
    printf("get(38): %d\n", v);

    int removed;
    open_remove(&t, 1, &removed);
    printf("remove(1): %d\n", removed);
    printf("size after remove: %zu\n", t.size);

    open_get(&t, 38, &v);
    printf("get(38) after remove: %d\n", v);

    open_put(&t, 14, 140, NULL);
    open_get(&t, 14, &v);
    printf("get(14): %d\n", v);
    printf("size after insert14: %zu\n", t.size);
    return 0;
}

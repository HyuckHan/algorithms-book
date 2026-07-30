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

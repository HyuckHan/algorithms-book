"""OpenAddressHashTable: linear probing, EMPTY/OCCUPIED/DELETED(tombstone),
integer key. lecture-notes/code/lecture07/java/OpenAddressHashMap.java와 같은
정책(첫 tombstone을 기억해두고 EMPTY까지 계속 probe한 뒤 재사용, probing load 기준 resize)을
따른다."""

EMPTY, OCCUPIED, DELETED = 0, 1, 2


# snippet:open-address-hash-table:start
class OpenAddressHashTable:
    _MAX_PROBING_LOAD = 0.65

    def __init__(self, capacity=8):
        self._keys = [None] * capacity
        self._values = [None] * capacity
        self._states = [EMPTY] * capacity
        self._size = 0
        self._tombstones = 0

    def __len__(self):
        return self._size

    def capacity(self):
        return len(self._keys)

    def tombstones(self):
        return self._tombstones

    def _home(self, key):
        return key % len(self._keys)

    def _find_index(self, key):
        m = len(self._keys)
        start = self._home(key)
        for i in range(m):
            j = (start + i) % m
            if self._states[j] == EMPTY:
                return -1
            if self._states[j] == OCCUPIED and self._keys[j] == key:
                return j
        return -1

    def get(self, key):
        j = self._find_index(key)
        return None if j < 0 else self._values[j]

    def put(self, key, value):
        if (self._size + self._tombstones + 1) / len(self._keys) > self._MAX_PROBING_LOAD:
            self._resize(len(self._keys) * 2)
        m = len(self._keys)
        start = self._home(key)
        first_deleted = -1
        for i in range(m):
            j = (start + i) % m
            if self._states[j] == OCCUPIED and self._keys[j] == key:
                old = self._values[j]
                self._values[j] = value
                return old
            if self._states[j] == DELETED and first_deleted < 0:
                first_deleted = j
            if self._states[j] == EMPTY:
                target = first_deleted if first_deleted >= 0 else j
                self._place(target, key, value)
                return None
        self._place(first_deleted, key, value)
        return None

    def _place(self, j, key, value):
        if self._states[j] == DELETED:
            self._tombstones -= 1
        self._keys[j] = key
        self._values[j] = value
        self._states[j] = OCCUPIED
        self._size += 1

    def remove(self, key):
        j = self._find_index(key)
        if j < 0:
            return None
        old = self._values[j]
        self._keys[j] = self._values[j] = None
        self._states[j] = DELETED
        self._size -= 1
        self._tombstones += 1
        return old

    def _resize(self, new_capacity):
        old_keys, old_values, old_states = self._keys, self._values, self._states
        self._keys = [None] * new_capacity
        self._values = [None] * new_capacity
        self._states = [EMPTY] * new_capacity
        self._size = self._tombstones = 0
        for k, v, s in zip(old_keys, old_values, old_states):
            if s == OCCUPIED:
                self.put(k, v)
# snippet:open-address-hash-table:end

if __name__ == "__main__":
    # NOTE: capacity()/tombstones() are deliberately not printed here -- the
    # reused Java/C implementations (lecture-notes/code/lecture07) each have
    # their own resize threshold/growth formula, so those internals can
    # differ in exact value across languages even on the same input. Only
    # map-level results (get/size/remove), which are policy-independent,
    # are printed -- run_examples.py requires the printed token sequence to
    # match exactly across all 3 languages.
    t = OpenAddressHashTable(capacity=8)
    for key in (25, 13, 16, 15, 7, 28, 31, 20, 1, 38):
        t.put(key, key * 10)
    print("size after inserts:", len(t))
    print("get(38):", t.get(38))
    print("remove(1):", t.remove(1))
    print("size after remove:", len(t))
    print("get(38) after remove:", t.get(38))
    t.put(14, 140)
    print("get(14):", t.get(14))
    print("size after insert14:", len(t))

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

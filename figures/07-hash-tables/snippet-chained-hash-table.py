class _Entry:
    def __init__(self, key, value, next_entry):
        self.key = key
        self.value = value
        self.next = next_entry


class ChainedHashTable:
    def __init__(self, capacity=7):
        self._buckets = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    def _index(self, key):
        return key % len(self._buckets)

    def _find(self, key):
        e = self._buckets[self._index(key)]
        while e is not None and e.key != key:
            e = e.next
        return e

    def get(self, key):
        e = self._find(key)
        return None if e is None else e.value

    def put(self, key, value):
        e = self._find(key)
        if e is not None:
            old = e.value
            e.value = value
            return old
        j = self._index(key)
        self._buckets[j] = _Entry(key, value, self._buckets[j])
        self._size += 1
        return None

    def remove(self, key):
        j = self._index(key)
        prev, e = None, self._buckets[j]
        while e is not None:
            if e.key == key:
                if prev is None:
                    self._buckets[j] = e.next
                else:
                    prev.next = e.next
                self._size -= 1
                return e.value
            prev, e = e, e.next
        return None

    def bucket_chain(self, index):
        keys = []
        e = self._buckets[index]
        while e is not None:
            keys.append(e.key)
            e = e.next
        return keys

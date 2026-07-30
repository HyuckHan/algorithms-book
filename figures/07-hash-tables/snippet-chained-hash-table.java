    private static final class Entry {
        final int key;
        int value;
        Entry next;
        Entry(int key, int value, Entry next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }

    private Entry[] buckets;
    private int size;

    public ChainedHashMap(int capacity) {
        buckets = new Entry[capacity];
    }

    private int index(int key) {
        return Math.floorMod(key, buckets.length);
    }

    private Entry find(int key) {
        for (Entry e = buckets[index(key)]; e != null; e = e.next)
            if (e.key == key) return e;
        return null;
    }

    public Integer get(int key) {
        Entry e = find(key);
        return e == null ? null : e.value;
    }

    public Integer put(int key, int value) {
        Entry old = find(key);
        if (old != null) {
            int previous = old.value;
            old.value = value;
            return previous;
        }
        int j = index(key);
        buckets[j] = new Entry(key, value, buckets[j]);
        size++;
        return null;
    }

    public Integer remove(int key) {
        int j = index(key);
        Entry previous = null;
        for (Entry e = buckets[j]; e != null; e = e.next) {
            if (e.key == key) {
                if (previous == null) buckets[j] = e.next;
                else previous.next = e.next;
                size--;
                return e.value;
            }
            previous = e;
        }
        return null;
    }

    public int size() { return size; }

    public List<Integer> bucketChain(int index) {
        List<Integer> keys = new ArrayList<>();
        for (Entry e = buckets[index]; e != null; e = e.next) keys.add(e.key);
        return keys;
    }

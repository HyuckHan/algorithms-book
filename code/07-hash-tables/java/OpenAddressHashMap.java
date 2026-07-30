/** lecture-notes/code/lecture07/java/OpenAddressHashMap.java와 같은 정책(linear
 * probing, EMPTY/OCCUPIED/DELETED tombstone, probing load 기준 resize)을 따르되
 * integer key 전용으로 단순화했다. */
public final class OpenAddressHashMap {
    private static final byte EMPTY = 0, OCCUPIED = 1, DELETED = 2;
    private static final double MAX_PROBING_LOAD = 0.65;

    // snippet:open-address-hash-table:start
    private int[] keys, values;
    private byte[] states;
    private int size, tombstones;

    public OpenAddressHashMap(int capacity) {
        keys = new int[capacity];
        values = new int[capacity];
        states = new byte[capacity];
    }

    private int home(int key) { return Math.floorMod(key, keys.length); }

    public int size() { return size; }

    private int findIndex(int key) {
        int start = home(key);
        for (int i = 0; i < keys.length; i++) {
            int j = (start + i) % keys.length;
            if (states[j] == EMPTY) return -1;
            if (states[j] == OCCUPIED && keys[j] == key) return j;
        }
        return -1;
    }

    public Integer get(int key) {
        int j = findIndex(key);
        return j < 0 ? null : values[j];
    }

    public Integer put(int key, int value) {
        if ((size + tombstones + 1.0) / keys.length > MAX_PROBING_LOAD) resize(keys.length * 2);

        int start = home(key), firstDeleted = -1;
        for (int i = 0; i < keys.length; i++) {
            int j = (start + i) % keys.length;
            if (states[j] == OCCUPIED && keys[j] == key) {
                int previous = values[j];
                values[j] = value;
                return previous;
            }
            if (states[j] == DELETED && firstDeleted < 0) firstDeleted = j;
            if (states[j] == EMPTY) {
                place(firstDeleted >= 0 ? firstDeleted : j, key, value);
                return null;
            }
        }
        place(firstDeleted, key, value);
        return null;
    }

    private void place(int j, int key, int value) {
        if (states[j] == DELETED) tombstones--;
        keys[j] = key;
        values[j] = value;
        states[j] = OCCUPIED;
        size++;
    }

    public Integer remove(int key) {
        int j = findIndex(key);
        if (j < 0) return null;
        int previous = values[j];
        states[j] = DELETED;
        size--;
        tombstones++;
        return previous;
    }

    private void resize(int newCapacity) {
        int[] oldKeys = keys, oldValues = values;
        byte[] oldStates = states;
        keys = new int[newCapacity];
        values = new int[newCapacity];
        states = new byte[newCapacity];
        size = tombstones = 0;
        for (int i = 0; i < oldKeys.length; i++)
            if (oldStates[i] == OCCUPIED) put(oldKeys[i], oldValues[i]);
    }
    // snippet:open-address-hash-table:end

    public static void main(String[] args) {
        OpenAddressHashMap t = new OpenAddressHashMap(8);
        for (int key : new int[] {25, 13, 16, 15, 7, 28, 31, 20, 1, 38}) t.put(key, key * 10);
        System.out.println("size after inserts: " + t.size());
        System.out.println("get(38): " + t.get(38));
        System.out.println("remove(1): " + t.remove(1));
        System.out.println("size after remove: " + t.size());
        System.out.println("get(38) after remove: " + t.get(38));
        t.put(14, 140);
        System.out.println("get(14): " + t.get(14));
        System.out.println("size after insert14: " + t.size());
    }
}

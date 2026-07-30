import java.util.ArrayList;
import java.util.List;

/** lecture-notes/code/lecture07/java/ChainedHashMap.java와 같은 정책(separate
 * chaining, head insertion, duplicate key는 update)을 따른다. capacity를 생성자로
 * 고정할 수 있게 하고, 데모용 bucketChain() 조회 메서드를 추가했다. */
public final class ChainedHashMap {
    // snippet:chained-hash-table:start
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
    // snippet:chained-hash-table:end

    private static String join(List<Integer> a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.size(); i++) { if (i > 0) sb.append(','); sb.append(a.get(i)); }
        return sb.toString();
    }

    public static void main(String[] args) {
        ChainedHashMap t = new ChainedHashMap(7);
        for (int key : new int[] {10, 17, 24}) t.put(key, key);
        System.out.println("bucket3 chain: " + join(t.bucketChain(3)));
        System.out.println("size: " + t.size());
        System.out.println("get(17): " + t.get(17));
        System.out.println("put(17,170) old: " + t.put(17, 170));
        System.out.println("get(17): " + t.get(17));
        System.out.println("remove(17): " + t.remove(17));
        System.out.println("bucket3 chain after remove: " + join(t.bucketChain(3)));
        System.out.println("size after remove: " + t.size());
    }
}

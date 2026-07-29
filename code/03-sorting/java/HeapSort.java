public final class HeapSort {
    // snippet:heap-sort:start
    /** MAX-HEAPIFY / BUILD-MAX-HEAP / Heapsort (1.5.3). This section's heap
     * array is explicitly 1-based (parent(i)=i/2, left(i)=2i, right(i)=2i+1,
     * per the Index convention callout), so instead of re-deriving 0-based
     * formulas, index 0 of the underlying array is left unused and heap
     * data occupies indices 1..n -- matching the pseudocode's index
     * arithmetic exactly rather than translating it. */
    static void swapAt(int[] a, int i, int j) {
        int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    }

    static void maxHeapify(int[] a, int i, int heapSize) {
        int l = 2 * i, r = 2 * i + 1, largest = i;
        if (l <= heapSize && a[l] > a[largest]) largest = l;
        if (r <= heapSize && a[r] > a[largest]) largest = r;
        if (largest != i) {
            swapAt(a, i, largest);
            maxHeapify(a, largest, heapSize);
        }
    }

    static void buildMaxHeap(int[] a, int n) {
        for (int i = n / 2; i >= 1; i--) {
            maxHeapify(a, i, n);
        }
    }

    static void heapSort(int[] a, int n) {
        buildMaxHeap(a, n);
        for (int last = n; last >= 2; last--) {
            swapAt(a, 1, last);
            maxHeapify(a, 1, last - 1);
        }
    }
    // snippet:heap-sort:end

    public static void main(String[] args) {
        int n = 10;
        int[] data = {0, 16, 14, 10, 8, 7, 9, 3, 2, 4, 1};
        System.out.println("input: " + toCsv(data, n));
        heapSort(data, n);
        System.out.println("heapsort: " + toCsv(data, n));
    }

    private static String toCsv(int[] a, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append(',');
            sb.append(a[i]);
        }
        return sb.toString();
    }
}

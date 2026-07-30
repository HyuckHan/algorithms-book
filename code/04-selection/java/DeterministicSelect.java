public final class DeterministicSelect {
    // snippet:deterministic-select:start
    /** lecture-notes/code/lecture04/c/deterministic_select.c의 알고리즘을 Java로
     * 옮긴 것이다(Median of Medians, group of 5). 최악의 경우에도 Theta(n)을
     * 보장한다. rank는 0-based(0..n-1). */
    static int deterministicSelect(int[] a, int rank) {
        return selectRange(a, 0, a.length, rank);
    }

    private static int selectRange(int[] a, int lo, int hi, int target) {
        while (true) {
            int n = hi - lo;
            if (n <= 5) {
                insertionSort(a, lo, hi);
                return a[target];
            }
            int groups = 0;
            for (int start = lo; start < hi; start += 5) {
                int end = Math.min(start + 5, hi);
                insertionSort(a, start, end);
                int median = start + (end - start - 1) / 2; // lower median
                swap(a, lo + groups, median);
                groups++;
            }
            // 그룹 median들의 median: 1-based ceil(groups/2)번째.
            int pivot = selectRange(a, lo, lo + groups, lo + (groups - 1) / 2);
            int[] equal = partition3(a, lo, hi, pivot);
            if (target < equal[0]) hi = equal[0];
            else if (target >= equal[1]) lo = equal[1];
            else return pivot;
        }
    }

    private static void insertionSort(int[] a, int lo, int hi) {
        for (int i = lo + 1; i < hi; i++) {
            int key = a[i]; int j = i;
            while (j > lo && a[j - 1] > key) { a[j] = a[j - 1]; j--; }
            a[j] = key;
        }
    }

    private static int[] partition3(int[] a, int lo, int hi, int pivot) {
        int lt = lo, scan = lo, gt = hi;
        while (scan < gt) {
            if (a[scan] < pivot) swap(a, lt++, scan++);
            else if (a[scan] > pivot) swap(a, scan, --gt);
            else scan++;
        }
        return new int[] {lt, gt};
    }

    private static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
    // snippet:deterministic-select:end

    public static void main(String[] args) {
        int[] data = {22, 4, 17, 9, 31, 12, 28, 6, 19, 2, 25, 1, 14, 30, 8,
                      16, 27, 5, 23, 10, 20, 3, 29, 7, 24};
        System.out.println("input: " + toCsv(data));
        int rank = 6;
        System.out.println("rank: " + rank);
        System.out.println("result: " + deterministicSelect(data, rank));
    }

    private static String toCsv(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(a[i]);
        }
        return sb.toString();
    }
}
